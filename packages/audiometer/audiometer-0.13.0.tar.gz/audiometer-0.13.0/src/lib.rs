use pyo3::prelude::*;

mod lufs;
mod sample;

// Integration time 300ms을 2를 나눈 값인 150ms 만큼 지수이동평균 적용
const INTEGRATION_TIME: f64 = 0.3 / 2.0;
// AES17에 따라 RMS 값에 +3dB를 적용하기 위한 보정값 (log10(2) = 0.3)
const AMPLITUDE_COEFFICIENT: f64 = 2.0;

fn ratio_to_db(ratio: f64, using_amplitude: bool) -> f64 {
    if ratio == 0.0 {
        return f64::INFINITY;
    }

    let logarithm = ratio.log10();
    let multiplier = if using_amplitude { 20.0 } else { 10.0 };

    multiplier * logarithm
}

#[pyfunction]
fn calculate_rms_inner(
    samples: Vec<isize>,
    channels: usize,
    max_amplitude: f64,
    sample_rate: isize,
) -> f64 {
    let decay_const = (-1.0 / sample_rate as f64 / INTEGRATION_TIME).exp();
    let update_ratio = 1.0 - decay_const;

    let mut max_rms: f64 = 0.0;
    for i in 0..channels {
        let mut channel_max_rms: f64 = 0.0;
        let mut current_rms: f64 = 0.0;
        for channel_sample in samples[i..].iter().step_by(channels) {
            let sample = (*channel_sample as f64 / max_amplitude).abs();
            current_rms = (current_rms * decay_const) + (sample * sample * update_ratio);
            channel_max_rms = channel_max_rms.max(current_rms);
        }

        max_rms = max_rms.max(channel_max_rms);
    }

    ratio_to_db(max_rms * AMPLITUDE_COEFFICIENT, false)
}

#[pyfunction]
fn calculate_peak_inner(samples: Vec<isize>, channels: usize, max_amplitude: f64) -> f64 {
    let mut max_peak: f64 = 0.0;
    for i in 0..channels {
        let mut channel_max_peak: f64 = 0.0;
        for channel_sample in samples[i..].iter().step_by(channels) {
            let sample = (*channel_sample as f64 / max_amplitude).abs();
            channel_max_peak = channel_max_peak.max(sample)
        }

        max_peak = max_peak.max(channel_max_peak)
    }

    ratio_to_db(max_peak, true)
}

/// A Python module implemented in Rust.
#[pymodule]
fn _audiometer(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_rms_inner, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_peak_inner, m)?)?;
    m.add_function(wrap_pyfunction!(lufs::parse_integrated_loudness, m)?)?;
    m.add_function(wrap_pyfunction!(lufs::parse_momentary_loudness, m)?)?;
    m.add_function(wrap_pyfunction!(sample::convert_24bit_to_32bit, m)?)?;
    Ok(())
}
