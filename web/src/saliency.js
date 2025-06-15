const tf = require('@tensorflow/tfjs');
const { loadClassifier } = require('./classify.js');

/**
 * Compute a Grad-CAM saliency heatmap for the input image tensor.
 * @param {tf.Tensor4D} input
 * @returns {Promise<tf.Tensor3D>} heatmap
 */
async function gradCAM(input) {
  const model = await loadClassifier();
  const convLayer = model.layers[model.layers.length - 2];
  const gradFunction = tf.grad(x => model.predict(x).max());
  const grads = gradFunction(input, convLayer);
  const pooled = tf.mean(grads, [0, 1, 2]);
  const activation = convLayer.output.mul(pooled);
  const heatmap = tf.relu(tf.sum(activation, -1));
  const normalized = heatmap.div(tf.max(heatmap));
  return normalized.squeeze();
}

module.exports = { gradCAM };
