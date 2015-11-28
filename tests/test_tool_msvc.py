import os

from tools_testcase import ToolTestCase, skipped

from aql import Tempdir, Tempfile, Project, ProjectConfig

# ==============================================================================


class TestToolMsvc(ToolTestCase):

    def test_msvc_compiler(self):
        with Tempdir() as tmp_dir:

            build_dir = os.path.join(tmp_dir, 'output')
            src_dir = os.path.join(tmp_dir, 'src')

            os.makedirs(src_dir)

            num_src_files = 5

            src_files, hdr_files = self.generate_cpp_files(
                src_dir, 'foo', num_src_files)
            res_file = self.generate_res_file(src_dir, 'foo')

            cfg = ProjectConfig(
                args=["build_dir=%s" % build_dir, "batch_build=0"])

            prj = Project(cfg)

            tools_path = os.path.join(os.path.dirname(__file__), '../tools')
            cpp = prj.tools.try_tool('msvc++', tools_path=tools_path)
            if cpp is None:
                skipped("MSVC tool has not been found.")
                return

            cpp.Compile(src_files, batch_build=False)
            cpp.CompileResource(res_file)

            self.build_prj(prj, num_src_files + 1)

            cpp.Compile(src_files)
            cpp.CompileResource(res_file)

            self.build_prj(prj, 0)

            self.touch_cpp_file(hdr_files[0])

            cpp.Compile(src_files)
            self.build_prj(prj, 1)

    # -----------------------------------------------------------

    def test_msvc_compiler_batch(self):
        with Tempdir() as tmp_dir:

            build_dir = os.path.join(tmp_dir, 'output')
            src_dir = os.path.join(tmp_dir, 'src')

            os.makedirs(src_dir)

            num_groups = 4
            group_size = 8
            num_src_files = num_groups * group_size

            src_files, hdr_files = self.generate_cpp_files(
                src_dir, 'foo', num_src_files)

            cfg = ProjectConfig(args=["build_dir=%s" % build_dir])

            prj = Project(cfg)

            tools_path = os.path.join(os.path.dirname(__file__),
                                      '../tools')
            cpp = prj.tools.try_tool('msvc++', tools_path=tools_path)
            if cpp is None:
                skipped("MSVC tool has not been found.")
                return

            cpp.Compile(src_files, batch_build=True)
            self.build_prj(prj, num_groups, jobs=num_groups)

            cpp.Compile(src_files, batch_build=False)
            self.build_prj(prj, 0)

            self.touch_cpp_file(hdr_files[0])
            cpp.Compile(src_files, batch_build=False)
            self.build_prj(prj, 1)

            self.touch_cpp_files(hdr_files[:group_size])

            cpp.Compile(src_files, batch_build=True, batch_groups=num_groups)
            self.build_prj(prj, num_groups)

    # -----------------------------------------------------------

    def test_msvc_compiler_batch_error(self):
        with Tempdir() as tmp_dir:

            build_dir = os.path.join(tmp_dir, 'output')
            src_dir = os.path.join(tmp_dir, 'src')

            cfg = ProjectConfig(args=["build_dir=%s" % build_dir])

            prj = Project(cfg)

            tools_path = os.path.join(os.path.dirname(__file__), '../tools')
            cpp = prj.tools.try_tool('msvc++', tools_path=tools_path)
            if cpp is None:
                skipped("MSVC tool has not been found.")

            os.makedirs(src_dir)

            num_src_files = 5

            src_files, hdr_files = self.generate_cpp_files(
                src_dir, 'foo', num_src_files)

            src_file_orig = Tempfile(root_dir=tmp_dir)
            src_file_orig.close()

            self.copy_file(src_files[0], src_file_orig)

            self.add_error_to_cpp_file(src_files[0])

            cpp.Compile(src_files, batch_build=True, batch_groups=1)

            self.build_prj(prj, 0, num_failed_nodes=1)

            self.copy_file(src_file_orig, src_files[0])

            cpp.Compile(src_files)

            self.build_prj(prj, 1)

    # -----------------------------------------------------------

    def test_msvc_archiver(self):
        with Tempdir() as tmp_dir:

            build_dir = os.path.join(tmp_dir, 'output')
            src_dir = os.path.join(tmp_dir, 'src')

            os.makedirs(src_dir)

            num_groups = 4
            group_size = 8
            num_src_files = num_groups * group_size

            src_files, hdr_files = self.generate_cpp_files(
                src_dir, 'foo', num_src_files)
            res_file = self.generate_res_file(src_dir, 'foo')

            cfg = ProjectConfig(args=["build_dir=%s" % build_dir])

            prj = Project(cfg)

            tools_path = os.path.join(os.path.dirname(__file__), '../tools')
            cpp = prj.tools.try_tool('msvc++', tools_path=tools_path)
            if cpp is None:
                skipped("MSVC tool has not been found.")

            cpp.LinkLibrary(src_files, res_file, target='foo',
                            batch_build=True, batch_groups=num_groups)

            self.build_prj(prj, num_groups + 2)

            cpp.LinkLibrary(src_files, res_file, target='foo')
            self.build_prj(prj, 0)

            self.touch_cpp_file(hdr_files[0])

            cpp.LinkLibrary(src_files, res_file, target='foo')
            self.build_prj(prj, 1)

            cpp.LinkLibrary(
                src_files, res_file, target='foo', batch_build=True)
            self.build_prj(prj, 0)

            self.touch_cpp_files(hdr_files)
            cpp.LinkLibrary(src_files, res_file, target='foo',
                            batch_build=True, batch_groups=num_groups)

            self.build_prj(prj, num_groups)

    # -----------------------------------------------------------

    def test_msvc_linker(self):
        with Tempdir() as tmp_dir:

            build_dir = os.path.join(tmp_dir, 'output')
            src_dir = os.path.join(tmp_dir, 'src')

            os.makedirs(src_dir)

            num_groups = 4
            group_size = 2
            num_src_files = num_groups * group_size

            src_files, hdr_files = self.generate_cpp_files(
                src_dir, 'foo', num_src_files)
            res_file = self.generate_res_file(src_dir, 'foo')
            main_src_file = self.generate_main_cpp_file(src_dir, 'main')

            cfg = ProjectConfig(
                args=["build_dir=%s" % build_dir, "batch_build=0"])

            prj = Project(cfg)

            tools_path = os.path.join(os.path.dirname(__file__), '../tools')
            cpp = prj.tools.try_tool('msvc++', tools_path=tools_path)
            if cpp is None:
                skipped("MSVC tool has not been found.")

            cpp.LinkSharedLibrary(src_files, res_file, target='foo')
            cpp.LinkSharedLibrary(src_files, res_file, target='foo')
            cpp.LinkProgram(src_files, main_src_file, res_file, target='foo')

            self.build_prj(prj, num_src_files + 4)

            cpp.LinkSharedLibrary(src_files, res_file, target='foo')
            cpp.LinkProgram(src_files, main_src_file, res_file, target='foo')
            self.build_prj(prj, 0)

            self.touch_cpp_file(hdr_files[0])

            cpp.LinkSharedLibrary(src_files, res_file, target='foo')
            cpp.LinkProgram(src_files, main_src_file, res_file, target='foo')
            self.build_prj(prj, 1)

            self.touch_cpp_files(hdr_files)

            cpp.LinkSharedLibrary(src_files, res_file, target='foo',
                                  batch_build=True, batch_groups=num_groups)

            cpp.LinkProgram(src_files, main_src_file, res_file, target='foo',
                            batch_build=True, batch_groups=num_groups)

            self.build_prj(prj, num_groups, jobs=1)

    # -----------------------------------------------------------

    def test_msvc_res_compiler(self):

        with Tempdir() as tmp_dir:

            build_dir = os.path.join(tmp_dir, 'build')
            src_dir = os.path.join(tmp_dir, 'src')
            os.makedirs(src_dir)

            num_src_files = 2

            src_files, hdr_files = self.generate_cpp_files(
                src_dir, 'foo', num_src_files)
            res_file = self.generate_res_file(src_dir, 'foo')

            cfg = ProjectConfig(args=["build_dir=%s" % build_dir])

            prj = Project(cfg)
            tools_path = os.path.join(os.path.dirname(__file__), '../tools')
            cpp = prj.tools.try_tool('msvc++', tools_path=tools_path)
            if cpp is None:
                skipped("MSVC tool has not been found.")

            tools_path = os.path.join(os.path.dirname(__file__), '../tools')
            rc = prj.tools.try_tool('msrc', tools_path=tools_path)
            if rc is None:
                skipped("MS RC tool has not been found.")

            cpp.Compile(src_files, batch_build=False)
            rc.Compile(res_file)
            self.build_prj(prj, num_src_files + 1)

            cpp.Compile(src_files, batch_build=False)
            rc.Compile(res_file)
            self.build_prj(prj, 0)

            cpp.Compile(src_files, batch_build=False)
            rc.Compile(res_file)
            self.touch_cpp_file(res_file)
            self.build_prj(prj, 1)

            cpp.Compile(src_files, batch_build=False)
            rc.Compile(res_file)
            self.build_prj(prj, 0)
