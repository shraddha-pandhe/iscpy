#!/usr/bin/env python

# Copyright (c) 2009, Purdue University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# Neither the name of the Purdue University nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import datetime

def ChangeVersionTag(start_dir, version_number):
  """Recursively goes through tags/release-version_number directory
  and replaces all #TRUNK# and TRUNK occurences with version_number

  Inputs:
    start_dir: tag directory. ex - 'tags/release-0.2'
    version_number: ex '0.2'
  """
  os.chdir(start_dir)

  for file_or_dir in os.listdir(os.getcwd()):
    if( not file_or_dir.startswith('.') ):
      if( os.path.isdir(file_or_dir) ):
        current_dir = os.getcwd()
        ChangeVersionTag(os.path.join(os.getcwd(), file_or_dir), version_number)
        os.chdir(current_dir)
      else:
        file_handle = open(file_or_dir, 'r')
        file_string = file_handle.read()
        file_handle.close()

        file_string = file_string.replace('#TRUNK#', version_number)
        file_string = file_string.replace('TRUNK', version_number)

        file_handle = open(file_or_dir, 'w')
        file_handle.write(file_string)
        file_handle.close()

release_number = raw_input('Specify release number: ')
release_dir = 'tags/release-%s' % release_number

#Doing the copying from trunk to tags
os.system('svn rm %s --force' % release_dir)
os.system('rm -rf %s' % release_dir)
os.system('svn copy trunk %s' % release_dir)

#Putting a timestamp in ChangeLog
file_handle = open(os.path.join(release_dir, 'ChangeLog'), 'r')
file_string = file_handle.read()
file_handle.close()

#Inserting today's timestamp at the top of the changes
file_string_parts = file_string.split('\n')
file_string_parts.insert(2, str(datetime.date.today()))
file_string = '\n'.join(file_string_parts)

file_handle = open(os.path.join(release_dir, 'ChangeLog'), 'w')
file_handle.write(file_string)
file_handle.close()

#Changing version tags
ChangeVersionTag(release_dir, release_number)

