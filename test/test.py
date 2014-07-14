#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, time, yaml

import wasanbon
from wasanbon.core import package, repositories

import unittest

test_dir = os.getcwd()

setting = yaml.load(open('setting.yaml', 'r'))
user_name = setting['user_name']
password = setting['password']


class TimeoutException(Exception):
    pass


class BinderCreateDeleteUseCase(unittest.TestCase):
    def setUp(self):
        sys.stdout.write('-------------- %s ---------------\n' % self.__class__.__name__)
        self.cwd = os.getcwd()
        pass


    def tearDown(self):
        os.chdir(self.cwd)
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', pack_name]), 0)
        self.assertFalse(pack_name in [p.name for p in package.get_packages()])
        pass

    def runTest(self):
        """
        RTCの作成と削除のテスト
        """
        pack_name = 'wasanbon_test_package'
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'create', pack_name]), 0)
        self.assertTrue(pack_name in [p.name for p in package.get_packages()])

        os.chdir(pack_name)
        back_end = 'python'
        comp_name = 'TestComponent'
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'create', comp_name]), 0)
        self.assertTrue(not package.get_package(pack_name).rtc(comp_name, suppress_exception=True) == None)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'addInPort', comp_name, 'RTC.TimedLong', 'in']), 0)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'addOutPort', comp_name, 'RTC.TimedLong', 'out']), 0)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'delete', comp_name]), 0)
        self.assertTrue(package.get_package(pack_name).rtc(comp_name, suppress_exception=True) == None)
        #os.chdir('..')
        #self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', pack_name]), 0)


class BinderCreateDeleteUseCase(unittest.TestCase):
    def setUp(self):
        sys.stdout.write('-------------- %s ---------------\n' % self.__class__.__name__)
        self.cwd = os.getcwd()
        pass


    def tearDown(self):
        os.chdir(self.cwd)
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'repository', 'destroy', '-f', '-u', user_name, '-p', password]), 0)
        pass

    def runTest(self):
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'repository', 'create', '-f', '-u', user_name, '-p', password]), 0)
        self.assertTrue(repositories.is_local_owner_repository(user_name))

        pack_name = 'wasanbon_test_package'
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'create', pack_name]), 0)
        self.assertTrue(pack_name in [p.name for p in package.get_packages()])

        os.chdir(pack_name)
        back_end = 'python'
        comp_name = 'TestComponent'
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'create', comp_name]), 0)
        self.assertTrue(not package.get_package(pack_name).rtc(comp_name, suppress_exception=True) == None)

        self.assertEqual(subprocess.call(['./mgr.py', 'repository', 'init', comp_name]), 0)
        self.assertEqual(subprocess.call(['./mgr.py', 'repository', 'remote_create', comp_name, '-u', user_name, '-p', password, '-v', '-n']), 0)

        from wasanbon.core.repositories import github_api
        g = github_api.GithubReference(user_name, password)
        g.get_repo(comp_name)

        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'addInPort', comp_name, 'RTC.TimedLong', 'in']), 0)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'addOutPort', comp_name, 'RTC.TimedLong', 'out']), 0)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'delete', comp_name]), 0)

        self.assertEqual(subprocess.call(['./mgr.py', 'repository', 'commit', comp_name, 'Test Commit']), 0)
        self.assertEqual(subprocess.call(['./mgr.py', 'repository', 'push', comp_name, '-u', user_name, '-p', password]), 0)
        self.assertTrue(package.get_package(pack_name).rtc(comp_name, suppress_exception=True) == None)
        
        self.assertEqual(subprocess.call(['./mgr.py', 'repository', 'remote_delete', comp_name, '-u', user_name, '-p', password, '-n', '-v']), 0)
        os.chdir('..')
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', pack_name]), 0)
        self.assertFalse(pack_name in [p.name for p in package.get_packages()])

        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'repository', 'destroy', '-f', '-u', user_name, '-p', password]), 0)
        pass

class BinderCreateDeleteUseCase(unittest.TestCase):
    pack_name = 'wasanbon_test_package'
    def setUp(self):
        sys.stdout.write('-------------- %s ---------------\n' % self.__class__.__name__)
        self.cwd = os.getcwd()
        pass


    def tearDown(self):
        os.chdir(self.cwd)
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'repository', 'destroy', '-f', '-u', user_name, '-p', password]), 0)
        pass


    def runTest(self):
        """
        github.comへのバインダーの作成と削除のテスト
        """
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'repository', 'create', '-f', '-u', user_name, '-p', password]), 0)
        self.assertTrue(repositories.is_local_owner_repository(user_name))


class PackageCreateDeleteUseCase(unittest.TestCase):
    pack_name = 'wasanbon_test_package'
    def setUp(self):
        sys.stdout.write('-------------- %s ---------------\n' % self.__class__.__name__)
        self.cwd = os.getcwd()
        pass


    def tearDown(self):
        os.chdir(self.cwd)
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', self.pack_name]), 0)
        self.assertFalse(self.pack_name in [p.name for p in package.get_packages()])
        pass


    def runTest(self):
        """
        パッケージの作成と削除テスト
        """
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'create', self.pack_name]), 0)
        self.assertTrue(self.pack_name in [p.name for p in package.get_packages()])



class CxxPackageUseCase(unittest.TestCase):
    pack_name = 'test_project01'
    """
    C++版のRTシステムのクローンと動作確認
    """
    def setUp(self):
        sys.stdout.write('-------------- %s ---------------\n' % self.__class__.__name__)
        self.cwd = os.getcwd()
        pass

    def tearDown(self):
        os.chdir(self.cwd)
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', self.pack_name]), 0)
        self.assertFalse(self.pack_name in [p.name for p in package.get_packages()])
        pass

    def runTest(self):
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'clone', self.pack_name]), 0)
        self.assertTrue(self.pack_name in [p.name for p in package.get_packages()])

        os.chdir(self.pack_name)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'build', 'all']), 0)
        for r in package.get_package(self.pack_name).rtcs:
            self.assertTrue(len(r.packageprofile.getRTCFilePath())!=0 or len(r.packageprofile.getRTCExecutableFilePath())!=0)

        p = subprocess.Popen(['./mgr.py', 'system', 'run', '-v'])
        i = 0
        while True:
            i = i+1
            if i > 450:
                raise TimeoutException()
            
            time.sleep(0.1)
            if os.path.isfile(os.path.join(os.getcwd(), 'testout.txt')):
                sys.stdout.write(' - testout.txt found. The value must be 1\n')
                f = open('testout.txt', 'r')
                self.assertEqual(f.read()[0:1], '1')
                break

        print ' - Terminating package'
        subprocess.call(['./mgr.py', 'system', 'terminate'])
        print ' - Waiting....'

        i = 0
        while True:
            i = i+1
            if i > 300:
                raise TimeoutException()
            time.sleep(0.1)
            p.poll()
            if p.returncode != None:
                break

        pass


class PythonPackageUseCase(unittest.TestCase):
    pack_name = 'test_project02'
    def setUp(self):
        sys.stdout.write('-------------- %s ---------------\n' % self.__class__.__name__)
        self.cwd = os.getcwd()
        pass

    def tearDown(self):
        os.chdir(self.cwd)
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', self.pack_name]), 0)
        self.assertFalse(self.pack_name in [p.name for p in package.get_packages()])

        pass


    def runTest(self):
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'clone', self.pack_name]), 0)
        self.assertTrue(self.pack_name in [p.name for p in package.get_packages()])

        os.chdir(self.pack_name)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'build', 'all']), 0)
        for r in package.get_package(self.pack_name).rtcs:
            self.assertTrue(len(r.packageprofile.getRTCFilePath())!=0 or len(r.packageprofile.getRTCExecutableFilePath())!=0)

        p = subprocess.Popen(['./mgr.py', 'system', 'run', '-v'])
        i = 0
        while True:
            i = i+1
            if i > 450:
                raise TimeoutException()

            time.sleep(0.1)
            if os.path.isfile(os.path.join(os.getcwd(), 'testout.txt')):
                sys.stdout.write(' - testout.txt found. The value must be 1\n')
                f = open('testout.txt', 'r')
                self.assertEqual(f.read()[0:1], '1')
                break

        print ' - Terminating'
        subprocess.call(['./mgr.py', 'system', 'terminate', '-v'])
        print ' - Waiting....'
        i = 0
        while True:
            i = i+1
            if i > 300:
                raise TimeoutException()
            time.sleep(0.1)
            p.poll()
            if p.returncode != None:
                break


class JavaPackageUseCase(unittest.TestCase):
    pack_name = 'test_project03'
    def setUp(self):
        sys.stdout.write('-------------- %s ---------------\n' % self.__class__.__name__)
        self.cwd = os.getcwd()
        pass

    def tearDown(self):
        os.chdir(self.cwd)
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'delete', self.pack_name]), 0)
        self.assertFalse(self.pack_name in [p.name for p in package.get_packages()])

        pass


    def runTest(self):
        self.assertEqual(subprocess.call(['wasanbon-admin.py', 'package', 'clone', self.pack_name]), 0)
        self.assertTrue(self.pack_name in [p.name for p in package.get_packages()])

        os.chdir(self.pack_name)
        self.assertEqual(subprocess.call(['./mgr.py', 'rtc', 'build', 'all']), 0)
        for r in package.get_package(self.pack_name).rtcs:
            self.assertTrue(len(r.packageprofile.getRTCFilePath())!=0 or len(r.packageprofile.getRTCExecutableFilePath())!=0)

        p = subprocess.Popen(['./mgr.py', 'system', 'run', '-v'])
        i = 0
        while True:
            i = i+1
            if i > 450:
                raise TimeoutException()

            time.sleep(0.1)
            if os.path.isfile(os.path.join(os.getcwd(), 'testout.txt')):
                sys.stdout.write(' - testout.txt found. The value must be 1\n')
                f = open('testout.txt', 'r')
                self.assertEqual(f.read()[0:1], '1')
                break

        print ' - Terminating'
        subprocess.call(['./mgr.py', 'system', 'terminate', '-v'])
        print ' - Waiting....'
        i = 0
        while True:
            i = i+1
            if i > 300:
                raise TimeoutException()
            time.sleep(0.1)
            p.poll()
            if p.returncode != None:
                break


if __name__ == '__main__':
    unittest.main()
