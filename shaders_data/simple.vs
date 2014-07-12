#version 120

varying vec4 vColor;

void main()
{
    float color = mod(floor(gl_Vertex[1]), 3.0);
    vColor = vec4(color, 0.0, 0.0, 1.0);
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
