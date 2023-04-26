import unittest

from pycompliance import pycompliance

class TestBenchmark(unittest.TestCase):

    def setUp(self) -> None:
        self.b = pycompliance.Benchmark('foo')
        return super().setUp()

    def test_benchmark_defaults(self):
        self.assertEqual(self.b.name, 'foo')
        self.assertIsNone(self.b.version)
        self.assertListEqual(self.b.children, [])

    def test_find_section(self):
        section = pycompliance.Section('1')
        self.b.add_section(section)
        subsection = pycompliance.Section('1.1')
        self.b.add_section(subsection)
        self.assertEqual(self.b.find('1.1'), subsection)

    def test_find_invalid_section_fails(self):
        self.assertEqual(self.b.find('1.1'), None)

    def test_find_control(self):
        section = pycompliance.Section('1')
        self.b.add_section(section)
        subsection = pycompliance.Section('1.1')
        control = pycompliance.Control('1.1.1')
        self.b.add_section(subsection)
        self.b.add_control(control)
        self.assertEqual(self.b.find('1.1.1'), control)

    def test_find_invalid_control_fails(self):
        section = pycompliance.Section('1')
        self.b.add_section(section)
        subsection = pycompliance.Section('1.1')
        self.b.add_section(subsection)
        self.assertEqual(self.b.find('1.1.1'), None)


class TestSection(unittest.TestCase):

    def test_default_section(self):
        s = pycompliance.Section('1')
        self.assertEqual(s.id, '1')
        self.assertIsNone(s.title)
        self.assertIsNone(s.description)
        self.assertListEqual(s.children, [])
        self.assertListEqual(s.children, [])

    def test_add_section(self):
        b = pycompliance.Benchmark('foo')
        s = pycompliance.Section('1')
        b.add_section(s)
        self.assertIn(s, b.children)

    def test_add_subsection_without_parent_section_fail(self):
        b = pycompliance.Benchmark('foo')
        s = pycompliance.Section('1.1')
        self.assertRaises(pycompliance.SectionNotFound, b.add_section, s)

    def test_add_subsection_with_parent(self):
        b = pycompliance.Benchmark('foo')
        parent = pycompliance.Section('1')
        child = pycompliance.Section('1.1')
        grandchild = pycompliance.Section('1.1.1')
        b.add_section(parent)
        b.add_section(child)
        b.add_section(grandchild)
        self.assertEqual(parent, b.find('1'))
        self.assertListEqual(parent.children, [child])
        self.assertEqual(child, b.find('1.1'))
        self.assertListEqual(child.children, [grandchild])
        self.assertEqual(grandchild, b.find('1.1.1'))
        self.assertListEqual(grandchild.children, [])

    def test_nested_sections(self):
        b = pycompliance.Benchmark('foo')
        s = pycompliance.Section('1')
        sub = pycompliance.Section('1.1')
        b.add_section(s)
        b.add_section(sub)
        self.assertIn(s, b.children)
        self.assertNotIn(sub, b.children)


class TestControl(unittest.TestCase):
    def test_default_control(self):
        c = pycompliance.Control('1.1.1')
        self.assertEqual(c.id, '1.1.1')
        self.assertIsNone(c.title)
        self.assertIsNone(c.description)
        self.assertIsNone(c.level)
        self.assertIsNone(c.remediation)
        self.assertIsNone(c.rationale)
        self.assertIsNone(c.audit)
        self.assertIsNone(c.assessment)

    def test_from_dict(self):
        d = {
            'id': '1.1.1',
        }
        c = pycompliance.Control.from_dict(d)
        self.assertEqual(c.id, '1.1.1')
        self.assertIsNone(c.title)
        self.assertIsNone(c.description)
        self.assertIsNone(c.level)
        self.assertIsNone(c.remediation)
        self.assertIsNone(c.rationale)
        self.assertIsNone(c.audit)
        self.assertIsNone(c.assessment)

    def test_from_dict_with_additional_keys(self):
        d = {
            'id': '1.1.1',
            'title': 'foo',
            'bar': True,
            'extra': 'metadata'
        }
        c = pycompliance.Control.from_dict(d)
        self.assertEqual(c.id, '1.1.1')
        self.assertEqual(c.title, 'foo')
        self.assertFalse(hasattr(c, 'bar'))
        self.assertFalse(hasattr(c, 'extra'))

    def test_from_dict_without_id_throws_exception(self):
        d = {}
        self.assertRaises(pycompliance.InvalidControlException, pycompliance.Control.from_dict, d)

    def test_control_with_invalid_id(self):
        # We should expect strings, not integers, floats, or boolean types for
        # IDs.
        for i in [1.1, 1, True, False]:
            self.assertRaises(pycompliance.InvalidControlException, pycompliance.Control, i)

    def test_add_control(self):
        b = pycompliance.Benchmark('foo')
        section = pycompliance.Section('1')
        subsection = pycompliance.Section('1.1')
        control = pycompliance.Control('1.1.1')
        b.add_section(section)
        b.add_section(subsection)
        b.add_control(control)
        self.assertListEqual(b.children, [section])
        self.assertListEqual(section.children, [subsection])
        self.assertListEqual(subsection.children, [control])

    def test_add_control_with_invalid_subsection_fails(self):
        b = pycompliance.Benchmark('foo')
        section = pycompliance.Section('1')
        control = pycompliance.Control('1.1.1')
        b.add_section(section)
        self.assertRaises(pycompliance.SectionNotFound, b.add_control, control)
