use cait_sith::protocol::Participant;
use k256::elliptic_curve::CurveArithmetic;
use k256::{AffinePoint, ProjectivePoint, Scalar, Secp256k1};
use pyo3::pyfunction;

use crate::{participant::convert_participants, participant::PyParticipant};

/// Get the lagrange coefficient for a participant, relative to this list.
fn lagrange(participants: &Vec<Participant>, p: &Participant) -> Scalar {
    let p_scalar = p.scalar::<Secp256k1>();

    let mut top = <Secp256k1 as CurveArithmetic>::Scalar::ONE;
    let mut bot = <Secp256k1 as CurveArithmetic>::Scalar::ONE;
    for q in participants {
        if p == q {
            continue;
        }
        let q_scalar = q.scalar::<Secp256k1>();
        top *= q_scalar;
        bot *= q_scalar - p_scalar;
    }

    top * bot.invert().unwrap()
}

#[pyfunction]
pub fn lagrange_calculation(participants: Vec<PyParticipant>, shares: Vec<String>) -> String {
    let participants: Vec<Participant> = convert_participants(participants);
    let shares: Vec<Scalar> = shares
        .iter()
        .map(|obj| serde_json::from_str(&obj).unwrap())
        .collect();

    let x: Scalar = participants
        .iter()
        .zip(shares)
        .map(|(p, s)| lagrange(&participants, p) * s)
        .sum();
    serde_json::to_string(&x).unwrap()
}

#[pyfunction]
pub fn multiply_by_generator(point: String) -> String {
    let point: Scalar = serde_json::from_str(&point).unwrap();
    let result = ProjectivePoint::GENERATOR * point;
    let result: AffinePoint = result.into();
    serde_json::to_string(&result).unwrap()
}

#[pyfunction]
pub fn multiply_two_points(a: String, b: String) -> String {
    let a: Scalar = serde_json::from_str(&a).unwrap();
    let b: Scalar = serde_json::from_str(&b).unwrap();
    let c = a * b;
    serde_json::to_string(&c).unwrap()
}

#[pyfunction]
pub fn invert(a: String) -> String {
    let a: Scalar = serde_json::from_str(&a).unwrap();
    let c = a.invert().unwrap();
    serde_json::to_string(&c).unwrap()
}
