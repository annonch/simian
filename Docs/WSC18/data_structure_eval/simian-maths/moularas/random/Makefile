# makefile for random library for Lua

# change these to reflect your Lua installation
#LUA= /tmp/lhf/lua-5.3.3
#LUAINC= $(LUA)/src
#LUALIB= $(LUA)/src
#LUABIN= $(LUA)/src

# these will probably work if Lua has been installed globally
LUA= /opt/local
LUAINC= $(LUA)/include
LUALIB= $(LUA)/lib
LUABIN= $(LUA)/bin

# probably no need to change anything below here
CC= gcc -std=c99
CFLAGS= $(INCS) $(WARN) -O2 $G
WARN= -Wall -Wextra
INCS= -I$(LUAINC)
MAKESO= $(CC) -shared
#MAKESO= $(CC) -bundle -undefined dynamic_lookup

MYNAME= random
MYLIB= l$(MYNAME)
T= $(MYNAME).so
OBJS= $(MYLIB).o
TEST= test.lua

all:	test

test:	$T
	$(LUABIN)/lua $(TEST)

o:	$(MYLIB).o

so:	$T

$T:	$(OBJS)
	$(MAKESO) -o $@ $(OBJS)

$(OBJS): random.c

clean:
	rm -f $(OBJS) $T core core.*

doc:
	@echo "$(MYNAME) library:"
	@fgrep '/**' $(MYLIB).c | cut -f2 -d/ | tr -d '*' | sort | column

# eof
