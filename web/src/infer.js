const { preprocess } = require('./preprocess.js');
const { detect } = require('./detect.js');
const { classify } = require('./classify.js');
const { gradCAM } = require('./saliency.js');

/**
 * Run the full inference pipeline on an image element.
 * @param {HTMLImageElement} img
 * @returns {Promise<object>} results
 */
async function runInference(img) {
  const input = preprocess(img);
  const [detections, cls, heatmap] = await Promise.all([
    detect(input),
    classify(input),
    gradCAM(input)
  ]);
  return { detections, cls, heatmap };
}

module.exports = { runInference };
