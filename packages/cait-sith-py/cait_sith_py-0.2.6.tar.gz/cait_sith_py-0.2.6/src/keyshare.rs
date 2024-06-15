use std::sync::{Arc, Mutex};

use cait_sith::protocol::Action;
use cait_sith::protocol::{MessageData, Participant, Protocol};
use cait_sith::KeygenOutput;
use k256::elliptic_curve::scalar::FromUintUnchecked;
use k256::elliptic_curve::CurveArithmetic;
use k256::sha2::{Digest, Sha256};
use k256::{AffinePoint, Scalar, Secp256k1, U256};
use pyo3::prelude::*;

use crate::{
    create_action_enum, create_protocol, participant::convert_participants,
    participant::PyParticipant,
};

#[pyclass(name = "KeyGenOutput")]
#[derive(Debug, Clone)]
pub struct PyKeygenOutput {
    #[pyo3(get)]
    pub private_share: String,
    #[pyo3(get)]
    pub public_key: String,
    _public_key: AffinePoint,
}

pub(crate) fn derive_epsilon(data: String) -> Scalar {
    let mut hasher = Sha256::new();
    hasher.update(data);
    return Scalar::from_uint_unchecked(U256::from_le_slice(&hasher.finalize()));
}

#[pymethods]
impl PyKeygenOutput {
    #[new]
    fn new(public_key: String, private_share: String) -> Self {
        Self {
            private_share,
            public_key: public_key.clone(),
            _public_key: serde_json::from_str(&public_key).unwrap(),
        }
    }

    fn derive_public_key(&self, user: String) -> String {
        let epsilon = derive_epsilon(user);
        let result = (<Secp256k1 as CurveArithmetic>::ProjectivePoint::GENERATOR * epsilon
            + self._public_key)
            .to_affine();
        serde_json::to_string(&result).unwrap()
    }
}

impl From<KeygenOutput<Secp256k1>> for PyKeygenOutput {
    fn from(value: KeygenOutput<Secp256k1>) -> Self {
        PyKeygenOutput {
            private_share: serde_json::to_string(&value.private_share).unwrap(),
            public_key: serde_json::to_string(&value.public_key).unwrap(),
            _public_key: value.public_key,
        }
    }
}

impl From<PyKeygenOutput> for KeygenOutput<Secp256k1> {
    fn from(value: PyKeygenOutput) -> Self {
        KeygenOutput {
            private_share: serde_json::from_str(&value.private_share).unwrap(),
            public_key: serde_json::from_str(&value.public_key).unwrap(),
        }
    }
}

create_action_enum!(KeygenAction, KeygenOutput<Secp256k1>, PyKeygenOutput);
create_protocol!(KeygenProtocol, KeygenOutput<Secp256k1>, KeygenAction);

/// The key generation protocol, with a given threshold.
///
/// This produces a new key pair, such that any set of participants
/// of size `>= threshold` can reconstruct the private key,
/// but no smaller set can do the same.
///
/// This needs to be run once, before then being able to perform threshold
/// signatures using the key.
#[pyfunction(name = "keygen")]
pub fn py_keygen(
    participants: Vec<PyParticipant>,
    me: PyParticipant,
    threshold: usize,
) -> PyResult<KeygenProtocol> {
    let participants: Vec<Participant> = convert_participants(participants);
    let me = me.into();
    let protocol = cait_sith::keygen(participants.as_slice(), me, threshold)
        .map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", err)))?;
    let wrapped = Arc::new(Mutex::new(protocol));
    Ok(KeygenProtocol { protocol: wrapped })
}
