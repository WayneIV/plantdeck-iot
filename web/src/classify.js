const tflite = require('@tensorflow/tfjs-tflite');
const tf = require('@tensorflow/tfjs');

let classifier;

async function loadClassifier() {
  if (!classifier) {
    classifier = await tflite.loadTFLiteModel('/models/mobilenetv2_bgrem.tflite');
  }
  return classifier;
}

async function classify(input) {
  const model = await loadClassifier();
  const logits = model.predict(input);
  const label = tf.argMax(logits, 1).dataSync()[0];
  const score = tf.max(logits, 1).dataSync()[0];
  return { label, score };
}

module.exports = { loadClassifier, classify };
