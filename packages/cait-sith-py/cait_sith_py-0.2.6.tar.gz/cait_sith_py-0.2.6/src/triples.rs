use std::sync::{Arc, Mutex};

use cait_sith::protocol::Action;
use cait_sith::protocol::{MessageData, Participant, Protocol};
use cait_sith::triples::{
    TripleGenerationOutput, TripleGenerationOutputMany, TriplePub, TripleShare,
};
use k256::Secp256k1;
use pyo3::prelude::*;
use pyo3::{pyclass, pyfunction, PyResult};
use serde::{Deserialize, Serialize};

use crate::{
    create_action_enum, create_protocol, participant::convert_participants,
    participant::PyParticipant,
};

#[pyclass(name = "TripleShare")]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct PyTripleShare {
    #[pyo3(get)]
    pub a: String,
    #[pyo3(get)]
    pub b: String,
    #[pyo3(get)]
    pub c: String,
}

impl From<TripleShare<Secp256k1>> for PyTripleShare {
    fn from(value: TripleShare<Secp256k1>) -> Self {
        Self {
            a: serde_json::to_string(&value.a).unwrap(),
            b: serde_json::to_string(&value.b).unwrap(),
            c: serde_json::to_string(&value.c).unwrap(),
        }
    }
}

impl From<PyTripleShare> for TripleShare<Secp256k1> {
    fn from(value: PyTripleShare) -> Self {
        Self {
            a: serde_json::from_str(&value.a).unwrap(),
            b: serde_json::from_str(&value.b).unwrap(),
            c: serde_json::from_str(&value.c).unwrap(),
        }
    }
}

#[pyclass(name = "TriplePublic")]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct PyTriplePublic {
    #[pyo3(get)]
    pub big_a: String,
    #[pyo3(get)]
    pub big_b: String,
    #[pyo3(get)]
    pub big_c: String,

    /// The participants in generating this triple.
    #[pyo3(get)]
    pub participants: Vec<PyParticipant>,
    /// The threshold which will be able to reconstruct it.
    #[pyo3(get)]
    pub threshold: usize,
}

impl From<TriplePub<Secp256k1>> for PyTriplePublic {
    fn from(value: TriplePub<Secp256k1>) -> Self {
        Self {
            big_a: serde_json::to_string(&value.big_a).unwrap(),
            big_b: serde_json::to_string(&value.big_b).unwrap(),
            big_c: serde_json::to_string(&value.big_c).unwrap(),
            participants: convert_participants(value.participants),
            threshold: value.threshold,
        }
    }
}

impl From<PyTriplePublic> for TriplePub<Secp256k1> {
    fn from(value: PyTriplePublic) -> Self {
        Self {
            big_a: serde_json::from_str(&value.big_a).unwrap(),
            big_b: serde_json::from_str(&value.big_b).unwrap(),
            big_c: serde_json::from_str(&value.big_c).unwrap(),
            participants: convert_participants(value.participants),
            threshold: value.threshold,
        }
    }
}

#[pyclass(name = "TripleGenerationOutput")]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PyTripleGenerationOutput {
    #[pyo3(get)]
    pub share: PyTripleShare,
    #[pyo3(get)]
    pub public: PyTriplePublic,
}

#[pyclass(name = "TripleGenerationOutputMany")]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PyTripleGenerationOutputMany {
    #[pyo3(get)]
    pub data: Vec<PyTripleGenerationOutput>,
}

#[pymethods]
impl PyTripleGenerationOutputMany {
    fn to_json(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }

    #[new]
    fn new(json_data: String) -> Self {
        serde_json::from_str(&json_data).unwrap()
    }
}

impl From<TripleGenerationOutputMany<Secp256k1>> for PyTripleGenerationOutputMany {
    fn from(value: TripleGenerationOutputMany<Secp256k1>) -> Self {
        Self {
            data: value.iter().map(|obj| obj.clone().into()).collect(),
        }
    }
}

#[pymethods]
impl PyTripleGenerationOutput {
    fn to_json(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }

    #[new]
    fn new(json_data: String) -> Self {
        serde_json::from_str(&json_data).unwrap()
    }
}

impl From<TripleGenerationOutput<Secp256k1>> for PyTripleGenerationOutput {
    fn from(value: TripleGenerationOutput<Secp256k1>) -> Self {
        Self {
            share: value.0.into(),
            public: value.1.into(),
        }
    }
}

impl From<PyTripleGenerationOutput> for TripleGenerationOutput<Secp256k1> {
    fn from(value: PyTripleGenerationOutput) -> Self {
        (value.share.into(), value.public.into())
    }
}

create_action_enum!(
    TripleGenerationActionMany,
    TripleGenerationOutputMany<Secp256k1>,
    PyTripleGenerationOutputMany
);

create_protocol!(
    TripleGenerationProtocolMany,
    TripleGenerationOutputMany<Secp256k1>,
    TripleGenerationActionMany
);

#[pyfunction(name = "generate_triple_many")]
pub fn py_generate_triple_many(
    participants: Vec<PyParticipant>,
    me: PyParticipant,
    threshold: usize,
    n: usize,
) -> PyResult<TripleGenerationProtocolMany> {
    let participants: Vec<Participant> = convert_participants(participants);
    let me = me.into();
    match n {
        1 => {
            let protocol = cait_sith::triples::generate_triple_many::<Secp256k1, 1>(
                participants.as_slice(),
                me,
                threshold,
            )
            .map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", err)))?;
            let wrapped = Arc::new(Mutex::new(protocol));
            Ok(TripleGenerationProtocolMany { protocol: wrapped })
        }
        10 => {
            let protocol = cait_sith::triples::generate_triple_many::<Secp256k1, 10>(
                participants.as_slice(),
                me,
                threshold,
            )
            .map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", err)))?;
            let wrapped = Arc::new(Mutex::new(protocol));
            Ok(TripleGenerationProtocolMany { protocol: wrapped })
        }
        50 => {
            let protocol = cait_sith::triples::generate_triple_many::<Secp256k1, 50>(
                participants.as_slice(),
                me,
                threshold,
            )
            .map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", err)))?;
            let wrapped = Arc::new(Mutex::new(protocol));
            Ok(TripleGenerationProtocolMany { protocol: wrapped })
        }
        100 => {
            let protocol = cait_sith::triples::generate_triple_many::<Secp256k1, 100>(
                participants.as_slice(),
                me,
                threshold,
            )
            .map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", err)))?;
            let wrapped = Arc::new(Mutex::new(protocol));
            Ok(TripleGenerationProtocolMany { protocol: wrapped })
        }
        1000 => {
            let protocol = cait_sith::triples::generate_triple_many::<Secp256k1, 1000>(
                participants.as_slice(),
                me,
                threshold,
            )
            .map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", err)))?;
            let wrapped = Arc::new(Mutex::new(protocol));
            Ok(TripleGenerationProtocolMany { protocol: wrapped })
        }
        _ => panic!("n ({n}) didn't match anything!"),
    }
}
