use crossbeam::{scope, thread};
use ndarray::{arr1, arr2, Array1, Array2, Axis};
use ndarray::{prelude::*, IndexLonger};
use ndarray_stats::QuantileExt;
use ndarray_stats::{DeviationExt, Quantile1dExt};
use numpy::ndarray::{ArrayViewD, ArrayViewMutD};
use ordered_float::OrderedFloat;
use rand::distributions::Uniform;
use rand::seq::SliceRandom;
use rand::{random, thread_rng, Rng};

use crate::episode::Episode;
type QTable = Array2<f64>;

const MODU: usize = 25_000;

#[derive(Debug)]
pub struct Qlearner {
    q_shape: (usize, usize),
    discount_factor: f64,
    learning_rate: f64,
    max_iterations: usize,
    quit_threshold: f64,
    verbose: bool,
}

type EpisodeLearnFn = fn(&Qlearner, &mut QTable, &Episode);

impl Qlearner {
    pub fn new(
        q_shape: (usize, usize),
        discount_factor: f64,
        learning_rate: f64,
        max_iterations: usize,
        quit_threshold: Option<f64>,
        verbose: bool,
    ) -> Self {
        let quit_threshold = quit_threshold.unwrap_or(0.001);
        Self {
            q_shape,
            discount_factor,
            learning_rate,
            max_iterations,
            quit_threshold,
            verbose,
        }
    }

    pub fn fast_learn(&self, episodes: &Vec<Episode>) -> QTable {
        let mut Q = QTable::zeros(self.q_shape.f());
        let mut Qsum = Vec::with_capacity(self.max_iterations / MODU + 1);

        for i in 0..self.max_iterations {
            // Choose a random episode
            let episode = episodes.choose(&mut thread_rng()).unwrap();
            // Learn from the episode
            self.learn_single_episode_forward_Q(&mut Q, episode);

            if i % MODU == 0 {
                Qsum.push(Q.sum());
                if i >= MODU * 2 && self.fast_can_stop_iterating(&Qsum, i) {
                    break;
                }
            }
        }
        Q
    }

    pub fn learn_until_convergence(&self, episodes: &Vec<Episode>) -> QTable {
        let mut Q = QTable::zeros(self.q_shape.f());
        let mut Qprev = Q.clone();

        for i in 0..self.max_iterations {
            // Choose a random episode
            let episode = episodes.choose(&mut thread_rng()).unwrap();
            // Learn from the episode
            self.learn_single_episode_forward_Q(&mut Q, episode);

            if i % MODU == 0 {
                let error = Q.mean_abs_err(&Qprev).unwrap();
                println!("{i}: {error}, {}, {}", Qprev.sum(), Q.sum() - Qprev.sum());
                if Q.abs_diff_eq(&Qprev, 1e-8) {
                    break;
                }
            }
            Qprev = Q.clone();
        }
        Q
    }

    fn fast_can_stop_iterating(&self, Qsum: &Vec<f64>, i: usize) -> bool {
        // Can stop iteration, as defined by Komorowski
        // Checks the relative change in Qsum over the last MODU iterations
        let i_check = i / MODU;
        let s = Qsum[i_check];
        let s_old = Qsum[i_check - 1];
        let d = (s - s_old) / s_old;
        if self.verbose {
            println!("Iteration: {}, Qsum: {}, d: {}", i, Qsum[i_check], d);
        }
        d.abs() < self.quit_threshold
    }

    pub fn learn(&self, episodes: &Vec<Episode>, method: EpisodeLearnFn) -> QTable {
        let mut Q = QTable::zeros(self.q_shape.f());
        let mut Qsum = Array::<f64, _>::zeros(self.max_iterations.f());
        for i in 0..self.max_iterations {
            // Choose a random episode
            let episode = episodes.choose(&mut thread_rng()).unwrap();
            // Learn from the episode
            method(self, &mut Q, episode);

            Qsum[[i]] = Q.sum();

            if i % MODU == 0 && i >= MODU * 2 && self.can_stop_iterating(&Qsum, i) {
                break;
            }
        }
        Q
    }

    pub fn learn_single_episode_forward_Q(&self, Q: &mut QTable, episode: &Episode) {
        for row in &episode.rows {
            let state_id = row.state_id;
            let action_id = row.action_id;
            let reward = row.reward;
            let next_state_id = row.next_state_id;
            let is_done = row.is_done;

            let old_value = Q[[state_id, action_id]];
            let new_value = if is_done {
                reward
            } else {
                reward + self.discount_factor * Qlearner::get_max_Q(Q, next_state_id)
            };

            Q[[state_id, action_id]] = old_value + self.learning_rate * (new_value - old_value);
        }
    }

    fn can_stop_iterating(&self, Qsum: &Array1<f64>, i: usize) -> bool {
        // Can stop iteration, as defined by Komorowski
        // Checks the relative change in Qsum over the last MODU iterations
        let s = Qsum.slice(s![i - MODU..i]).mean().unwrap();
        let s_old = Qsum.slice(s![i - 2 * MODU..i - MODU]).mean().unwrap();
        let d = (s - s_old) / s_old;
        if self.verbose {
            println!("Iteration: {}, Qsum: {}, d: {}", i, Qsum[[i]], d);
        }
        d.abs() < self.quit_threshold
    }

    fn get_max_Q(Q: &QTable, state_id: usize) -> f64 {
        let state_row = Q.index_axis(Axis(0), state_id);
        state_row.fold(std::f64::MIN, |acc, &x| acc.max(x))
    }

    pub fn learn_single_episode_backward_TD(&self, Q: &mut QTable, episode: &Episode) {
        // Get reward of last row
        let mut return_t = episode.rows[episode.rows.len() - 1].reward;

        for i in (0..episode.rows.len() - 1).rev() {
            let row = &episode.rows[i];
            let state_id = row.state_id;
            let action_id = row.action_id;
            let reward = row.reward;

            // Perform q update
            Q[[state_id, action_id]] = (1.0 - self.learning_rate) * Q[[state_id, action_id]]
                + self.learning_rate * return_t;

            // Update return for time t- 1
            // Express it in terms of return and time t and reward achieved at time t - 1
            return_t = reward + self.discount_factor * return_t;
        }
    }

    pub fn learn_parallel(
        &self,
        episodes: &Vec<Episode>,
        method: EpisodeLearnFn,
        iter_ql: usize,
    ) -> Array3<f64> {
        let result: Vec<Array2<_>> = scope(|s| {
            let handles: Vec<_> = (0..iter_ql)
                .map(|_| s.spawn(move |_| self.learn(episodes, method)))
                .collect();
            handles.into_iter().map(|h| h.join().unwrap()).collect()
        })
        .expect("Error in fetching all results");

        // Convert Vec of Array2 to Array3
        let mut result_array = Array3::<f64>::zeros((iter_ql, self.q_shape.0, self.q_shape.1).f());
        for (i, Q) in result.into_iter().enumerate() {
            // This clones I think
            result_array.slice_mut(s![i, .., ..]).assign(&Q);
        }
        result_array
    }

    pub fn td_learn_backward_parallel(
        &self,
        episodes: Vec<Episode>,
        boostrap_sample_size: usize,
        iter_ql: usize,
    ) -> Array3<f64> {
        let result: Vec<Array2<_>> = scope(|s| {
            let mut handles = Vec::with_capacity(iter_ql);
            for _ in 0..iter_ql {
                // Sample episodes for td_learn_backward
                let episode_clone = episodes.clone();
                let sample_indices = sample_indices(episodes.len(), boostrap_sample_size);
                // TODO: sampling right now clones all episodes: slow
                let sample: Vec<_> = sample_indices
                    .iter()
                    .map(|&i| episode_clone[i].clone())
                    .collect();

                let handle = s.spawn(move |_| {
                    self.learn(&sample, Qlearner::learn_single_episode_backward_TD)
                });
                handles.push(handle);
            }
            handles.into_iter().map(|h| h.join().unwrap()).collect()
        })
        .expect("Error in fetching all results");

        // Convert Vec of Array2 to Array3
        let mut result_array = Array3::<f64>::zeros((iter_ql, self.q_shape.0, self.q_shape.1).f());
        for (i, Q) in result.into_iter().enumerate() {
            // This clones I think
            result_array.slice_mut(s![i, .., ..]).assign(&Q);
        }
        result_array
    }

    fn learn_single_episode_forward_Q_lambda(&self, Q: &mut QTable, episode: &Episode) {
        // Apply the Q lambda learning method to a single episode
        // TODO: requires importance sampling afaik as i know, so cannot implement 123
    }

    pub fn double_q(&self, episodes: &Vec<Episode>) -> QTable {
        let mut Qtable1 = QTable::zeros(self.q_shape.f());
        let mut Qtable2 = QTable::zeros(self.q_shape.f());

        for i in 0..self.max_iterations {
            // Choose a random episode
            let episode = episodes.choose(&mut thread_rng()).unwrap();

            // Choose random value between 0 and 1
            self.double_q_single_episode(&mut Qtable1, &mut Qtable2, episode);
            if i % MODU == 0 {
                println!(
                    "Iteration: {}, Qsum1 {}, Qsum2 {}",
                    i,
                    Qtable1.sum(),
                    Qtable2.sum()
                );
            }
        }

        // Return average of Qtable1 and Qtable2
        (Qtable1 + Qtable2) / 2.0
    }

    fn double_q_single_episode(
        &self,
        Qtable1: &mut QTable,
        Qtable2: &mut QTable,
        episode: &Episode,
    ) {
        // Apply the double Q learning method to a single episode
        for row in &episode.rows {
            let state_id = row.state_id;
            let action_id = row.action_id;
            let reward = row.reward;
            let next_state_id = row.next_state_id;
            let is_done = row.is_done;

            let random_value: f32 = thread_rng().gen();

            if random_value < 0.5 {
                // Update Qtable1
                // Uses old value and best action of Qtable1
                // Evaluates action on Qtable2
                let old_value = Qtable1[[state_id, action_id]];
                let target = if is_done {
                    reward
                } else {
                    let best_action = Qlearner::get_best_action(Qtable1, next_state_id);
                    reward + self.discount_factor * Qtable2[[next_state_id, best_action]]
                };
                // Compute new value as Qtable1[s, a] + learning_rate * (Qtable1[s', argmax(Qtable2[s'])] - Qtable1[s, a])
                let new_value = old_value + self.learning_rate * (target - old_value);
                Qtable1[[state_id, action_id]] = new_value;
            } else {
                // Update Qtable2
                // Uses old value and best action of Qtable2
                // Evaluates action on Qtable1
                let old_value = Qtable2[[state_id, action_id]];
                let target = if is_done {
                    reward
                } else {
                    let best_action = Qlearner::get_best_action(Qtable2, next_state_id);
                    reward + self.discount_factor * Qtable1[[next_state_id, best_action]]
                };
                // Compute new value as Qtable2[s, a] + learning_rate * (Qtable2[s', argmax(Qtable1[s'])] - Qtable2[s, a])
                let new_value = old_value + self.learning_rate * (target - old_value);
                Qtable2[[state_id, action_id]] = new_value;
            }
        }
    }

    fn get_best_action(Qtable: &mut QTable, state_id: usize) -> usize {
        // Get the best action for a given state
        // Argmax of Qtable[state, :]
        let state_row = Qtable.index_axis(Axis(0), state_id);
        let best_action = state_row.argmax().unwrap();
        best_action
    }

    pub fn learn_single_episode_expected_sarsa(&self, Q: &mut QTable, episode: &Episode) {
        for row in &episode.rows {
            let state_id = row.state_id;
            let action_id = row.action_id;
            let reward = row.reward;
            let next_state_id = row.next_state_id;
            let is_done = row.is_done;

            let old_value = Q[[state_id, action_id]];
            let target = if is_done {
                reward
            } else {
                let mean_Q = Q.index_axis(Axis(0), state_id).mean().unwrap();
                reward + self.discount_factor * mean_Q
            };

            Q[[state_id, action_id]] = old_value + self.learning_rate * (target - old_value);
        }
    }
}

fn sample_indices(num_total_episodes: usize, sample_size: usize) -> Vec<usize> {
    // Generate sample_size number between 0 and num_total_episodes - 1
    let rng = rand::thread_rng();
    let distribution = Uniform::from(0..num_total_episodes);
    rng.sample_iter(distribution).take(sample_size).collect()
}
