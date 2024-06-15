use cait_sith::protocol::Participant;
use pyo3::pyclass::CompareOp;
use pyo3::{pyclass, pymethods, IntoPy, PyObject, Python};
use serde::{Deserialize, Serialize};

/// Represents a participant in the protocol.
///
/// Each participant should be uniquely identified by some number, which this
/// struct holds. In our case, we use a `u32`, which is enough for billions of
/// participants. That said, you won't actually be able to make the protocols
/// work with billions of users.
#[pyclass(name = "Participant")]
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Hash, Deserialize)]
pub struct PyParticipant {
    #[pyo3(get)]
    id: u32,
}

#[pymethods]
impl PyParticipant {
    #[new]
    #[pyo3(signature = (id), text_signature = "(id:int)")]
    fn new(id: u32) -> Self {
        PyParticipant { id }
    }

    fn __richcmp__(&self, other: &Self, op: CompareOp, py: Python<'_>) -> PyObject {
        match op {
            CompareOp::Eq => (self.id == other.id).into_py(py),
            CompareOp::Ne => (self.id != other.id).into_py(py),
            _ => py.NotImplemented(),
        }
    }

    fn __hash__(&self) -> u64 {
        self.id as u64
    }
}

impl From<Participant> for PyParticipant {
    fn from(value: Participant) -> Self {
        PyParticipant { id: value.into() }
    }
}

impl From<PyParticipant> for Participant {
    fn from(value: PyParticipant) -> Self {
        value.id.into()
    }
}

pub fn convert_participants<S: Clone, T: From<S>>(data: Vec<S>) -> Vec<T> {
    data.iter().map(|obj| obj.clone().into()).collect()
}
