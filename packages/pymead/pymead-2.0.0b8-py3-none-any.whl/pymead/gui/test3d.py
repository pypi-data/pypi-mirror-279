import math

import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *


def main():
    app = pg.mkQApp("GLShaders Example")
    w = gl.GLViewWidget()
    w.show()
    w.setWindowTitle('pyqtgraph example: GL Shaders')
    w.setCameraPosition(distance=15, azimuth=-90)

    g = gl.GLGridItem()
    g.scale(2, 2, 1)
    w.addItem(g)

    md = gl.MeshData.sphere(rows=10, cols=20)
    x = np.linspace(-8, 8, 6)

    sigma = 0.5
    twoSigSq = 2. * sigma * sigma

    def dampedOscillation(u, v, t):
        """Calculation of a R2 -> R1 function at position u,v at curr_time t.

        A t-dependent cosine function is multiplied with a 2D gaussian.
        Both functions depend on the distance of (u,v) to the origin."""

        distSq = u * u + v * v
        dist = math.pi * 4 * math.sqrt(distSq)
        return 0.5 * math.exp(-distSq / twoSigSq) * math.cos(dist - t)

    nPts = 15
    degree = 4
    samplingTolerance = 2.0
    xMin, xMax, yMin, yMax = -1.0, 1.0, -1.0, 1.0
    xStep = (xMax - xMin) / (nPts - 1)
    yStep = (yMax - yMin) / (nPts - 1)

    # initialise a list representing a regular 2D grid of control points.
    controlPoints = [ \
        [[yMin + y * yStep, xMin + x * xStep, 0.0] for x in range(nPts)] \
        for y in range(nPts)]

    # initialise knots ...
    knots = [0.0 for i in range(int(degree / 2))] + \
            [float(i) / (nPts - 1) for i in range(nPts)] + \
            [1.0 for i in range(int((degree + 1) / 2))]

    # initialise enclosing
    enclosing = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]

    # first trim curve is a circle
    angleNum = 16
    angles = [-2 * math.pi * float(i) / angleNum for i in range(angleNum)]
    radius = 0.05
    offset = (0.4, 0.6)
    circleDegree = degree
    circlePoints = [ \
        [offset[0] + radius * math.cos(theta), offset[1] + radius * math.sin(theta)] \
        for theta in angles]
    for i in range(circleDegree - 1):
        circlePoints = circlePoints + [circlePoints[i]]
    knotNum = len(circlePoints) + circleDegree
    circleKnots = [float(i) / (knotNum - 1) for i in range(knotNum)]

    # second trim curve is a square
    squareHolePoints = [[0.4, 0.4], [0.4, 0.45], [0.45, 0.45], \
                        [0.45, 0.4], [0.4, 0.4]]

    def updateControlPoints(t):
        """Calculate function values for all 2D grid points."""
        for row in controlPoints:
            for coord in row:
                coord[2] = dampedOscillation(coord[0], coord[1], t)

    def plotSurface(t):
        # display surface
        updateControlPoints(t)
        nurb = gluNewNurbsRenderer()

        gluBeginSurface(nurb)
        gluNurbsSurface(nurb, knots, knots, controlPoints, GL_MAP2_VERTEX_3)

        # trim curve enclosing
        gluBeginTrim(nurb)
        gluPwlCurve(nurb, enclosing, GLU_MAP1_TRIM_2)
        gluEndTrim(nurb)

        # trim using square
        gluBeginTrim(nurb)
        gluPwlCurve(nurb, squareHolePoints, GLU_MAP1_TRIM_2)
        gluEndTrim(nurb)

        # trim using circle
        gluBeginTrim(nurb)
        gluNurbsCurve(nurb, circleKnots, circlePoints, GLU_MAP1_TRIM_2)
        gluEndTrim(nurb)

        gluEndSurface(nurb)

        return nurb

    n = plotSurface(0.0)

    md2 = gl.MeshData(vertexes=n)

    m1 = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 0, 0, 0.2), shader='balloon', glOptions='additive')
    m1.translate(x[0], 0, 0)
    m1.scale(1, 1, 2)
    w.addItem(m1)

    pg.exec()


if __name__ == "__main__":
    main()
