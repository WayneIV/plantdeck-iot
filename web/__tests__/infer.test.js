global.self = { location: { origin: '' } };

jest.mock('@tensorflow/tfjs', () => ({}));
jest.mock('@tensorflow/tfjs-tflite', () => ({
  loadTFLiteModel: jest.fn(() => Promise.resolve({ predict: jest.fn(() => [ {arraySync:()=>[]}, {arraySync:()=>[]} ]) }))
}));

jest.mock('../src/preprocess.js');
jest.mock('../src/detect.js');
jest.mock('../src/classify.js');
jest.mock('../src/saliency.js');

const { runInference } = require('../src/infer.js');
const { preprocess } = require('../src/preprocess.js');
const { detect } = require('../src/detect.js');
const { classify } = require('../src/classify.js');
const { gradCAM } = require('../src/saliency.js');

test('runInference aggregates module results', async () => {
  preprocess.mockReturnValue('input');
  detect.mockResolvedValue([{ box: [0,0,1,1], score: 0.9 }]);
  classify.mockResolvedValue({ label: 1, score: 0.8 });
  gradCAM.mockResolvedValue('heatmap');

  const img = {};
  const res = await runInference(img);

  expect(res.detections).toHaveLength(1);
  expect(res.cls.label).toBe(1);
  expect(res.heatmap).toBe('heatmap');
});
