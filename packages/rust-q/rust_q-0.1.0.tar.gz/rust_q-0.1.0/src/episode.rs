use numpy::PyReadonlyArray2;

#[derive(Debug, Clone)]
pub struct Row {
    pub state_id: usize,
    pub action_id: usize,
    pub reward: f64,
    pub next_state_id: usize,
    pub is_done: bool,
}

#[derive(Debug, Clone)]
pub struct Episode {
    pub rows: Vec<Row>,
}

pub fn to_episode(data: PyReadonlyArray2<f64>) -> Episode {
    let rows = data
        .as_array()
        .rows()
        .into_iter()
        .map(|row| {
            let state_id = row[0] as usize;
            let action_id = row[1] as usize;
            let reward = row[2];
            let next_state_id = row[3] as usize;
            let is_done = row[4] == 1.0;
            Row {
                state_id,
                action_id,
                reward,
                next_state_id,
                is_done,
            }
        })
        .collect::<Vec<_>>();
    Episode { rows }
}

pub fn to_episodes(data: Vec<PyReadonlyArray2<f64>>) -> Vec<Episode> {
    data.into_iter().map(to_episode).collect()
}
