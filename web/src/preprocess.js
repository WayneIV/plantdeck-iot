const tf = require('@tensorflow/tfjs');

/**
 * Preprocess an image for model input.
 * - Converts HTMLImageElement to tensor
 * - Performs simple background removal
 * - Resizes to 224x224 and normalizes
 * @param {HTMLImageElement} img
 * @returns {tf.Tensor4D}
 */
function preprocess(img) {
  const tensor = tf.browser.fromPixels(img);
  const resized = tf.image.resizeBilinear(tensor, [224, 224]);
  const channels = tf.split(resized, 3, 2);
  const mask = channels[1].greater(tf.scalar(10));
  const filtered = resized.mul(mask);
  const normalized = filtered.div(255);
  return normalized.expandDims(0);
}

module.exports = { preprocess };
