const tflite = require('@tensorflow/tfjs-tflite');
const tf = require('@tensorflow/tfjs');

let detector;

async function loadDetector() {
  if (!detector) {
    detector = await tflite.loadTFLiteModel('/models/yolov8_disease.tflite');
  }
  return detector;
}

function nms(boxes, scores, iouThreshold = 0.5) {
  const selected = [];
  let idxs = scores.map((s, i) => [s, i]).sort((a, b) => b[0] - a[0]);
  while (idxs.length) {
    const [, idx] = idxs.shift();
    selected.push(idx);
    idxs = idxs.filter(([s, i]) => {
      const iou = boxIou(boxes[idx], boxes[i]);
      return iou < iouThreshold;
    });
  }
  return selected;
}

function boxIou(a, b) {
  const [ax1, ay1, ax2, ay2] = a;
  const [bx1, by1, bx2, by2] = b;
  const areaA = Math.max(0, ax2 - ax1) * Math.max(0, ay2 - ay1);
  const areaB = Math.max(0, bx2 - bx1) * Math.max(0, by2 - by1);
  const ix1 = Math.max(ax1, bx1);
  const iy1 = Math.max(ay1, by1);
  const ix2 = Math.min(ax2, bx2);
  const iy2 = Math.min(ay2, by2);
  const inter = Math.max(0, ix2 - ix1) * Math.max(0, iy2 - iy1);
  return inter / (areaA + areaB - inter + 1e-6);
}

async function detect(input) {
  const model = await loadDetector();
  const output = model.predict(input);
  const [boxes, scores] = output;
  const boxesArr = boxes.arraySync();
  const scoresArr = scores.arraySync();
  const keep = nms(boxesArr, scoresArr);
  return keep.map(i => ({ box: boxesArr[i], score: scoresArr[i] }));
}

module.exports = { loadDetector, detect };
