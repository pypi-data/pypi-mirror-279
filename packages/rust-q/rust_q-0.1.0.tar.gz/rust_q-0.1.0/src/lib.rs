use ndarray::{self, Array2};
use numpy::{IntoPyArray, PyArray2, PyArray3, PyReadonlyArray2};
use pyo3::prelude::*;

use crate::{
    episode::{to_episodes, Episode},
    qlearning::Qlearner,
};

mod episode;
mod qlearning;

// NOTE
// * numpy defaults to np.float64, if you use other type than f64 in Rust
//   you will have to change type in Python before calling the Rust function.

// The name of the module must be the same as the rust package name
#[pymodule]
fn rust_q(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn qlearn_forward<'py>(
        py: Python<'py>,
        data: Vec<PyReadonlyArray2<f64>>,
        q_shape: (usize, usize),
        discount_factor: f64,
        learning_rate: f64,
        max_iterations: usize,
        verbose: bool,
        quit_threshold: Option<f64>,
    ) -> &'py PyArray2<f64> {
        let episodes = to_episodes(data);
        let learner = Qlearner::new(
            q_shape,
            discount_factor,
            learning_rate,
            max_iterations,
            quit_threshold,
            verbose,
        );
        let QTable = learner.learn(&episodes, Qlearner::learn_single_episode_forward_Q);
        QTable.into_pyarray(py)
    }

    #[pyfn(m)]
    fn td_learn_backward<'py>(
        py: Python<'py>,
        data: Vec<PyReadonlyArray2<f64>>,
        q_shape: (usize, usize),
        discount_factor: f64,
        learning_rate: f64,
        max_iterations: usize,
        verbose: bool,
        quit_threshold: Option<f64>,
    ) -> &'py PyArray2<f64> {
        let episodes = to_episodes(data);
        let learner = Qlearner::new(
            q_shape,
            discount_factor,
            learning_rate,
            max_iterations,
            quit_threshold,
            verbose,
        );
        let QTable = learner.learn(&episodes, Qlearner::learn_single_episode_backward_TD);
        QTable.into_pyarray(py)
    }

    #[pyfn(m)]
    fn expected_sarsa<'py>(
        py: Python<'py>,
        data: Vec<PyReadonlyArray2<f64>>,
        q_shape: (usize, usize),
        discount_factor: f64,
        learning_rate: f64,
        max_iterations: usize,
        verbose: bool,
        quit_threshold: Option<f64>,
    ) -> &'py PyArray2<f64> {
        let episodes = to_episodes(data);
        let learner = Qlearner::new(
            q_shape,
            discount_factor,
            learning_rate,
            max_iterations,
            quit_threshold,
            verbose,
        );
        let QTable = learner.learn(&episodes, Qlearner::learn_single_episode_expected_sarsa);
        QTable.into_pyarray(py)
    }

    #[pyfn(m)]
    fn td_learn_backward_parallel<'py>(
        py: Python<'py>,
        data: Vec<PyReadonlyArray2<f64>>,
        q_shape: (usize, usize),
        discount_factor: f64,
        learning_rate: f64,
        max_iterations: usize,
        boostrap_sample_size: usize,
        iter_ql: usize,
        verbose: bool,
        quit_threshold: Option<f64>,
    ) -> &'py PyArray3<f64> {
        let episodes = to_episodes(data);
        let learner = qlearning::Qlearner::new(
            q_shape,
            discount_factor,
            learning_rate,
            max_iterations,
            quit_threshold,
            verbose,
        );
        let QTables = learner.td_learn_backward_parallel(episodes, boostrap_sample_size, iter_ql);
        QTables.into_pyarray(py)
    }

    #[pyfn(m)]
    fn qlearn_forward_parallel<'py>(
        py: Python<'py>,
        data: Vec<PyReadonlyArray2<f64>>,
        q_shape: (usize, usize),
        discount_factor: f64,
        learning_rate: f64,
        max_iterations: usize,
        ql_iter: usize,
        verbose: bool,
        quit_threshold: Option<f64>,
    ) -> &'py PyArray3<f64> {
        let episodes = to_episodes(data);
        let learner = Qlearner::new(
            q_shape,
            discount_factor,
            learning_rate,
            max_iterations,
            quit_threshold,
            verbose,
        );
        println!("Q learning forward parallel, config: {:?}", learner);
        let QTable =
            learner.learn_parallel(&episodes, Qlearner::learn_single_episode_forward_Q, ql_iter);
        QTable.into_pyarray(py)
    }

    #[pyfn(m)]
    fn fast_learn<'py>(
        py: Python<'py>,
        data: Vec<PyReadonlyArray2<f64>>,
        q_shape: (usize, usize),
        discount_factor: f64,
        learning_rate: f64,
        max_iterations: usize,
        verbose: bool,
        quit_threshold: Option<f64>,
    ) -> &'py PyArray2<f64> {
        let episodes = to_episodes(data);
        let learner = Qlearner::new(
            q_shape,
            discount_factor,
            learning_rate,
            max_iterations,
            quit_threshold,
            verbose,
        );
        let QTable = learner.fast_learn(&episodes);
        QTable.into_pyarray(py)
    }

    #[pyfn(m)]
    fn learn_until_convergence<'py>(
        py: Python<'py>,
        data: Vec<PyReadonlyArray2<f64>>,
        q_shape: (usize, usize),
        discount_factor: f64,
        learning_rate: f64,
        max_iterations: usize,
        verbose: bool,
        quit_threshold: Option<f64>,
    ) -> &'py PyArray2<f64> {
        let episodes = to_episodes(data);
        let learner = Qlearner::new(
            q_shape,
            discount_factor,
            learning_rate,
            max_iterations,
            quit_threshold,
            verbose,
        );
        let QTable = learner.learn_until_convergence(&episodes);
        QTable.into_pyarray(py)
    }

    #[pyfn(m)]
    fn double_q<'py>(
        py: Python<'py>,
        data: Vec<PyReadonlyArray2<f64>>,
        q_shape: (usize, usize),
        discount_factor: f64,
        learning_rate: f64,
        max_iterations: usize,
        verbose: bool,
        quit_threshold: Option<f64>,
    ) -> &'py PyArray2<f64> {
        let episodes = to_episodes(data);
        let learner = Qlearner::new(
            q_shape,
            discount_factor,
            learning_rate,
            max_iterations,
            quit_threshold,
            verbose,
        );
        let QTable = learner.double_q(&episodes);
        QTable.into_pyarray(py)
    }

    Ok(())
}
