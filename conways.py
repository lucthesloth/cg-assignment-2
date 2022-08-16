import numpy as np
import moderngl
import moderngl_window as mglw


class Conway(mglw.WindowConfig):
    title = "Compute Shader - Conway's Game of Life"
    window_size = 1280, 720

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.update_delay = 1 / 60
        self.last_updated = 0
        self.width, self.height = 640, 360
        self.wnd.fixed_aspect_ratio = self.width / self.height
        pixels = np.round(np.random.rand(self.width, self.height)).astype('f4')
        self.display_prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 i_v;
                in vec2 i_tc;
                out vec2 v_text;
                void main() {
                    v_text = i_tc;
                    gl_Position = vec4(i_v, 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                uniform sampler2D t;
                in vec2 v_text;
                out vec4 f_color;
                void main() {
                    f_color = texture(t, v_text);
                }
            ''',
        )
        self.transform_prog = self.ctx.program(
            vertex_shader='''
                #version 330
                uniform sampler2D t;
                out float out_vert;
                #define ALIVE 1.0
                #define DEAD 0.0
                bool cell(int x, int y) {
                    ivec2 tSize = textureSize(t, 0).xy;
                    return texelFetch(t, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0).r > 0.5;
                }
                void main() {
                    int width = textureSize(t, 0).x;
                    ivec2 i_t = ivec2(gl_VertexID % width, gl_VertexID / width);
                    bool isAlive = cell(i_t.x, i_t.y);
                    int n = 0;
                    if (cell(i_t.x - 1, i_t.y - 1)) n++;
                    if (cell(i_t.x - 1, i_t.y + 0)) n++;
                    if (cell(i_t.x - 1, i_t.y + 1)) n++;
                    if (cell(i_t.x + 1, i_t.y - 1)) n++;
                    if (cell(i_t.x + 1, i_t.y + 0)) n++;
                    if (cell(i_t.x + 1, i_t.y + 1)) n++;
                    if (cell(i_t.x + 0, i_t.y + 1)) n++;
                    if (cell(i_t.x + 0, i_t.y - 1)) n++;
                    if (isAlive) {
                        out_vert = (n < 4 && n > 1) ? ALIVE : DEAD;
                    } else {
                        out_vert = (n == 3) ? ALIVE : DEAD;
                    }
                }
            ''',
            varyings=['out_vert']
        )

        self.texture = self.ctx.texture(
            (self.width, self.height), 1, pixels.tobytes(), dtype='f4')
        self.texture.filter = moderngl.NEAREST, moderngl.NEAREST
        self.texture.swizzle = 'RRR1'

        self.vbo = self.ctx.buffer(np.array([
            -1.0, -1.0,  0, 0,
            -1.0,  1.0,  0, 1,
            1.0,  -1.0,  1, 0,
            1.0,   1.0,  1, 1,
        ], dtype="f4"))
        self.vao = self.ctx.simple_vertex_array(
            self.display_prog, self.vbo, 'i_v', 'i_tc')

        self.tao = self.ctx.vertex_array(self.transform_prog, [])
        self.pbo = self.ctx.buffer(reserve=pixels.nbytes)

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)

        self.texture.use(location=0)

        if time - self.last_updated > self.update_delay:
            self.tao.transform(self.pbo, vertices=self.width * self.height)
            self.texture.write(self.pbo)
            self.last_updated = time

        self.vao.render(moderngl.TRIANGLE_STRIP)


if __name__ == '__main__':
    Conway.run()
