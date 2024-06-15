use std::sync::{Arc, Mutex};

use crate::{create_action_enum, create_protocol};
use cait_sith::protocol::Participant;
use cait_sith::{
    protocol::Action, protocol::MessageData, protocol::Protocol, PresignArguments, PresignOutput,
};

use k256::Secp256k1;
use pyo3::{pyclass, pyfunction, pymethods, PyErr, PyResult};
use serde::{Deserialize, Serialize};

use crate::{participant::convert_participants, participant::PyParticipant};

use crate::keyshare::{derive_epsilon, PyKeygenOutput};
use crate::triples::PyTripleGenerationOutput;

/// The arguments needed to create a presignature.
#[pyclass(name = "PresignArguments")]
#[derive(Debug, Clone)]
pub struct PyPresignArguments {
    /// The first triple's public information, and our share.
    pub triple0: PyTripleGenerationOutput,
    /// Ditto, for the second triple.
    pub triple1: PyTripleGenerationOutput,
    /// The output of key generation, i.e. our share of the secret key, and the public key.
    pub keygen_output: PyKeygenOutput,
    /// The desired threshold for the presignature, which must match the original threshold
    pub threshold: usize,
}

#[pymethods]
impl PyPresignArguments {
    #[new]
    fn new(
        triple0: PyTripleGenerationOutput,
        triple1: PyTripleGenerationOutput,
        keygen_output: PyKeygenOutput,
        threshold: usize,
    ) -> Self {
        Self {
            triple0,
            triple1,
            keygen_output,
            threshold,
        }
    }
}

impl From<PyPresignArguments> for PresignArguments<Secp256k1> {
    fn from(value: PyPresignArguments) -> Self {
        Self {
            triple0: value.triple0.into(),
            triple1: value.triple1.into(),
            keygen_out: value.keygen_output.into(),
            threshold: value.threshold,
        }
    }
}

/// The output of the presigning protocol.
///
/// This output is basically all the parts of the signature that we can perform
/// without knowing the message.
#[pyclass(name = "PresignOutput")]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PyPresignOutput {
    /// The public nonce commitment.
    #[pyo3(get)]
    pub big_r: String,
    /// Our share of the nonce value.
    #[pyo3(get)]
    pub k: String,
    /// Our share of the sigma value.
    #[pyo3(get)]
    pub sigma: String,
}

impl From<PresignOutput<Secp256k1>> for PyPresignOutput {
    fn from(value: PresignOutput<Secp256k1>) -> Self {
        Self {
            big_r: serde_json::to_string(&value.big_r).unwrap(),
            k: serde_json::to_string(&value.k).unwrap(),
            sigma: serde_json::to_string(&value.sigma).unwrap(),
        }
    }
}

impl From<PyPresignOutput> for PresignOutput<Secp256k1> {
    fn from(value: PyPresignOutput) -> Self {
        Self {
            big_r: serde_json::from_str(&value.big_r).unwrap(),
            k: serde_json::from_str(&value.k).unwrap(),
            sigma: serde_json::from_str(&value.sigma).unwrap(),
        }
    }
}

#[pymethods]
impl PyPresignOutput {
    fn derive_for_user(&self, data: String) -> PyPresignOutput {
        let view: PresignOutput<Secp256k1> = self.clone().into();
        let epsilon = derive_epsilon(data);

        let derived_presign = PresignOutput {
            big_r: view.big_r,
            k: view.k,
            sigma: view.sigma + epsilon * view.k,
        };

        derived_presign.into()
    }

    fn to_json(&self) -> String {
        serde_json::to_string(&self).unwrap()
    }

    #[new]
    fn new(json_data: String) -> Self {
        serde_json::from_str(&json_data).unwrap()
    }
}

create_action_enum!(
    PresignGenerationAction,
    PresignOutput<Secp256k1>,
    PyPresignOutput
);

create_protocol!(
    PresignGenerationProtocol,
    PresignOutput<Secp256k1>,
    PresignGenerationAction
);

#[pyfunction(name = "presign")]
pub fn py_presign(
    participants: Vec<PyParticipant>,
    me: PyParticipant,
    args: PyPresignArguments,
) -> PyResult<PresignGenerationProtocol> {
    let participants: Vec<Participant> = convert_participants(participants);
    let me = me.into();
    let args = args.into();
    let protocol = cait_sith::presign(
        participants.as_slice(),
        me,
        participants.as_slice(),
        me,
        args,
    )
    .map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", err)))?;
    let wrapped = Arc::new(Mutex::new(protocol));
    Ok(PresignGenerationProtocol { protocol: wrapped })
}
