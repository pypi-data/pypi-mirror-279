import unittest
import trimesh
from your_module import MeshTestCase

class TestMeshTestCase(MeshTestCase):
    def setUp(self):
        # create two box mesh objects for testing
        self.mesh1 = trimesh.creation.box(extents=[1,1,1])
        self.mesh2 = trimesh.creation.box(extents=[1,1,1])

        # create two Node objects (assumed to be the structure in your module)
        self.node1 = Node()
        self.node1.mesh = self.mesh1

        self.node2 = Node()
        self.node2.mesh = self.mesh2

    def test_assertIntersects(self):
        self.assertIntersects(self.node1, self.node2)

    def test_assertIntersects_fail(self):
        with self.assertRaises(AssertionError):
            self.assertIntersects(self.node1, self.node2)

    def test_assertInside(self):
        self.assertInside(self.node1, self.node2)

    def test_assertInside_fail(self):
        with self.assertRaises(AssertionError):
            self.assertInside(self.node1, self.node2)

    def test_assertClose(self):
        self.assertClose(self.node1, self.node2)

    def test_assertClose_fail(self):
        with self.assertRaises(AssertionError):
            self.assertClose(self.node1, self.node2)

    def test_assertFar(self):
        self.assertFar(self.node1, self.node2)

    def test_assertFar_fail(self):
        with self.assertRaises(AssertionError):
            self.assertFar(self.node1, self.node2)

    def test_assertIntersectionVolume(self):
        self.assertIntersectionVolume(self.node1, self.node2)

    def test_assertIntersectionVolume_fail(self):
        with self.assertRaises(AssertionError):
            self.assertIntersectionVolume(self.node1, self.node2)

if __name__ == '__main__':
    unittest.main()
