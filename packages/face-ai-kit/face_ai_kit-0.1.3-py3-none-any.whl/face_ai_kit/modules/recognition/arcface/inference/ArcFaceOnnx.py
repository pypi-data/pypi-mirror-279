
from ..ArcFace import ArcFace

import onnxruntime as ort

class ArcFaceOnnx(ArcFace):

    def __init__(self, inf, model_path) -> None:
        super().__init__(inf, model_path)
        
        providers = list()
        if inf=='onnx-cpu':
            providers = ['CPUExecutionProvider']
        elif inf=='onnx-gpu':
            providers = ['CUDAExecutionProvider']
        else:
            raise  RuntimeError("Face recognition: Unkown provider")

        self.session = ort.InferenceSession(model_path, providers=providers)
        
    def infer(self, face_img):

        self._t['forward_pass'].tic()
        outputs = self.session.run(None, {'face_input': face_img})
        self._t['forward_pass'].toc()

        return outputs

