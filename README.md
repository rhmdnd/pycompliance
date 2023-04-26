# pycompliance

A simply library to represent compliance benchmarks as tree structures.

```python
from pycompliance import pycompliance

benchmark = pycompliance.Benchmark("CIS Red Hat OpenShift Container Platform")
benchmark.version = "1.3.0"

section = pycompliance.Section("1")
section.title = "Control Plane Components"
benchmark.add_section(section)

subsection = pycompliance.Section("1.1")
subsection.title = "Master Node Configuration Files"
benchmark.add_section(subsection)

control = pycompliance.Control("1.1.1")
control.title = "Ensure foobar permissions"
benchmark.add_control(control)

print(benchmark.find('1.1.1').title)
```

Outputs:

```console
Ensure foobar permissions
```
