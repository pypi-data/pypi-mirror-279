use crate::participant::{convert_participants, PyParticipant};
use crate::presign::PyPresignOutput;
use crate::{create_action_enum, create_protocol};
use cait_sith::{CSCurve, FullSignature};
use k256::elliptic_curve::ops::Reduce;
use k256::elliptic_curve::Curve;
use k256::{ PublicKey, Scalar, Secp256k1};
use pyo3::{pyclass, pyfunction};

use std::sync::{Arc, Mutex};

use cait_sith::protocol::{Action, Participant};
use cait_sith::protocol::{MessageData, Protocol};
use k256::ecdsa::signature::Verifier;
use k256::ecdsa::{Signature, VerifyingKey};
use k256::elliptic_curve::point::AffineCoordinates;
use pyo3::prelude::*;
use pyo3::PyResult;

/// Represents a signature with extra information, to support different variants of ECDSA.
///
/// An ECDSA signature is usually two scalars. The first scalar is derived from
/// a point on the curve, and because this process is lossy, some other variants
/// of ECDSA also include some extra information in order to recover this point.
///
/// Furthermore, some signature formats may disagree on how precisely to serialize
/// different values as bytes.
///
/// To support these variants, this simply gives you a normal signature, along with the entire
/// first point.
#[pyclass(name = "FullSignature")]
#[derive(Clone, Debug)]
pub struct PyFullSignature {
    /// This is the entire first point.
    #[pyo3(get)]
    pub big_r: String,
    /// This is the second scalar, normalized to be in the lower range.
    #[pyo3(get)]
    pub s: String,
}

impl From<FullSignature<Secp256k1>> for PyFullSignature {
    fn from(value: FullSignature<Secp256k1>) -> Self {
        Self {
            big_r: serde_json::to_string(&value.big_r).unwrap(),
            s: serde_json::to_string(&value.s).unwrap(),
        }
    }
}

create_action_enum!(SignAction, FullSignature<Secp256k1>, PyFullSignature);

create_protocol!(SignProtocol, FullSignature<Secp256k1>, SignAction);

impl From<PyFullSignature> for FullSignature<Secp256k1> {
    fn from(value: PyFullSignature) -> Self {
        Self {
            big_r: serde_json::from_str(&value.big_r).unwrap(),
            s: serde_json::from_str(&value.s).unwrap(),
        }
    }
}

fn x_coordinate<C: CSCurve>(point: &C::AffinePoint) -> C::Scalar {
    <C::Scalar as Reduce<<C as Curve>::Uint>>::reduce_bytes(&point.x())
}

#[pyfunction(name = "verify")]
pub fn py_verify(signature: PyFullSignature, public_key: String, msg: Vec<u8>) {
    let signature: FullSignature<Secp256k1> = signature.into();
    let public_key = serde_json::from_str(&public_key).unwrap();
    let sig = Signature::from_scalars(x_coordinate::<Secp256k1>(&signature.big_r), signature.s)
        .expect("Couldn't convert signature");
    VerifyingKey::from(&PublicKey::from_affine(public_key).unwrap())
        .verify(&msg[..], &sig)
        .unwrap();
}

/// The signature protocol, allowing us to use a presignature to sign a message.
///
/// **WARNING** You must absolutely hash an actual message before passing it to
/// this function. Allowing the signing of arbitrary scalars *is* a security risk,
/// and this function only tolerates this risk to allow for genericity.
#[pyfunction(name = "sign")]
pub fn py_sign(
    participants: Vec<PyParticipant>,
    me: PyParticipant,
    public_key: String,
    presignature: PyPresignOutput,
    msg_hash: Vec<u8>,
) -> PyResult<SignProtocol> {
    let participants: Vec<Participant> = convert_participants(participants);
    let me = me.into();
    let public_key = serde_json::from_str(&public_key).unwrap();
    let presignature = presignature.into();
    let msg_hash =
        <Scalar as Reduce<<Secp256k1 as Curve>::Uint>>::reduce_bytes(msg_hash.as_slice().into());

    let protocol = cait_sith::sign(
        participants.as_slice(),
        me,
        public_key,
        presignature,
        msg_hash,
    )
    .map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", err)))?;

    let wrapped = Arc::new(Mutex::new(protocol));
    Ok(SignProtocol { protocol: wrapped })
}
