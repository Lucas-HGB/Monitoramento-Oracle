def execute_command(cursor, command):
	cursor.execute("%s"% command)
	return cursor.fetchall()


def choose_script(cursor, opc, value = 0):

	if opc.lower() == 'opendatabase':
		value = execute_command(cursor, """select open_mode from v$database""")

	elif opc.lower() == 'asm_perc_used':
		value = execute_command(cursor, """select NAME,to_char(round(((TOTAL_MB-FREE_MB)*100)/TOTAL_MB),'FM99999999999999990')||'%' PERC_USED
                from asm order by 2
""")

	elif opc.lower() == 'asm_perc_used_name':
		value = execute_command(cursor, """select to_char(round(((TOTAL_MB-FREE_MB)*100)/TOTAL_MB),'FM99999999999999990') from  asm where NAME='%s'""" % value)

	elif opc.lower() == 'tbs_perc_used':
		value = execute_command(cursor, """select to_char(round(used_percent),'FM99999999999999990') retvalue 
	     from dba_tablespace_usage_metrics 
	     where tablespace_name ='%s'
""" % value)

	elif opc.lower() == 'tbs_size_used':
		value = execute_command(cursor, """select to_char(round(tablespace_size*(select VALUE from v$parameter where NAME='db_block_size')),'FM99999999999999990') retvalue 
	     from dba_tablespace_usage_metrics 
	     where tablespace_name ='%s' 
""" % value)

	elif opc.lower() == 'tbs_size_total':
		value = execute_command(cursor, """select to_char(round(tablespace_size*(select VALUE from v$parameter where NAME='db_block_size')),'FM99999999999999990') retvalue 
	     from dba_tablespace_usage_metrics 
	     where tablespace_name ='%s' 
""" % value)

	elif opc.lower() == 'valpar':
		value = execute_command(cursor, """SELECT value FROM v$parameter WHERE name='%s'""" % value)

	elif opc.lower() == 'checkactive':
		value = execute_command(cursor, """select to_char(case when inst_cnt > 0 then 1 else 0 end,'FM99999999999999990') retvalue
             from (select count(*) inst_cnt from v$instance 
                   where status = 'OPEN' and logins = 'ALLOWED' and database_status = 'ACTIVE')
""")

	elif opc.lower() == 'version':
		value = execute_command(cursor, """select banner from gv$version where rownum=1""")

	elif opc.lower() == 'uptime':
		value = execute_command(cursor, """select to_char((sysdate-startup_time)*86400, 'FM99999999999999990') retvalue from gvinstance""")

	elif opc.lower() == 'rcachehit':
		value = execute_command(cursor, """SELECT to_char((1 - (phy.value - lob.value - dir.value) / ses.value) * 100, 'FM99999990.9999') retvalue
            FROM   v$sysstat ses, v$sysstat lob,
                   v$sysstat dir, v$sysstat phy
            WHERE  ses.name = 'session logical reads'
            AND    dir.name = 'physical reads direct'
            AND    lob.name = 'physical reads direct (lob)'
            AND    phy.name = 'physical reads'
""")

	elif opc.lower() == 'dsksortratio':
		value = execute_command(cursor, """SELECT to_char(d.value/(d.value + m.value)*100, 'FM99999990.9999') retvalue
             FROM  v$sysstat m, v$sysstat d
             WHERE m.name = 'sorts (memory)'
             AND d.name = 'sorts (disk)'
""")

	elif opc.lower() == 'activeusercount':
		value = execute_command(cursor, """select to_char(count(*)-1, 'FM99999999999999990') retvalue from v$session where username is not null 
             and status='ACTIVE' 
""")

	elif opc.lower() == 'usercount':
		value = execute_command(cursor, """select to_char(count(*)-1, 'FM99999999999999990') retvalue from v$session where username is not null""")

	elif opc.lower() == 'dbsize':
		value = execute_command(cursor, """SELECT to_char(sum(  NVL(a.bytes - NVL(f.bytes, 0), 0)), 'FM99999999999999990') retvalue
             FROM sys.dba_tablespaces d,
             (select tablespace_name, sum(bytes) bytes from dba_data_files group by tablespace_name) a,
             (select tablespace_name, sum(bytes) bytes from dba_free_space group by tablespace_name) f
             WHERE d.tablespace_name = a.tablespace_name(+) AND d.tablespace_name = f.tablespace_name(+)
             AND NOT (d.extent_management like 'LOCAL' AND d.contents like 'TEMPORARY')
""")

	elif opc.lower() == 'dbfilesize':
		value = execute_command(cursor, """select to_char(sum(bytes), 'FM99999999999999990') retvalue from dba_data_files""")

	elif opc.lower() == 'commits':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'user commits'""")

	elif opc.lower() == 'rollbacks':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'user rollbacks'""")

	elif opc.lower() == 'deadlocks':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'enqueue deadlocks'""")

	elif opc.lower() == 'redowrites':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'redo writes'""")

	elif opc.lower() == 'tblscans':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'table scans (long tables)'""")

	elif opc.lower() == 'tblrowsscans':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'table scan rows gotten'""")

	elif opc.lower() == 'indexffs':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'index fast full scans (full)'""")

	elif opc.lower() == 'hparsratio':
		value = execute_command(cursor, """SELECT to_char(h.value/t.value*100,'FM99999990.9999') retvalue
             FROM  v$sysstat h, v$sysstat t
             WHERE h.name = 'parse count (hard)'
             AND t.name = 'parse count (total)'
""")

	elif opc.lower() == 'netsent':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'bytes sent via SQL*Net to client'""")

	elif opc.lower() == 'netresv':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'bytes received via SQL*Net from client'""")

	elif opc.lower() == 'netroundtrips':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'SQL*Net roundtrips to/from client'""")

	elif opc.lower() == 'logonscurrent':
		value = execute_command(cursor, """select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'logons current'""")

	elif opc.lower() == 'lastarclog':
		value = execute_command(cursor, """select to_char(max(SEQUENCE#), 'FM99999999999999990') retvalue from v$log where archived = 'YES'""")

	elif opc.lower() == 'lastapplarclog':
		value = execute_command(cursor, """select to_char(max(lh.SEQUENCE#), 'FM99999999999999990') retvalue
             from v$loghist lh, v$archived_log al
             where lh.SEQUENCE# = al.SEQUENCE# and applied='YES'
""")

	elif opc.lower() == 'freebufwaits':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'free buffer waits'
""")

	elif opc.lower() == 'bufbusywaits':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'buffer busy waits'
""")

	elif opc.lower() == 'logswcompletion':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'log file switch completion'
""")

	elif opc.lower() == 'logfilesync':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'log file sync'
""")

	elif opc.lower() == 'logprllwrite':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'log file parallel write'
""")

	elif opc.lower() == 'performance':
		value = execute_command(cursor, """select to_char(AVERAGE, 'FM99999999999999990') retvalue
             from v$sysmetric_summary where metric_id=%s and group_id=2
""" % value)

	elif opc.lower() == 'lockblock':
		value = execute_command(cursor, """SELECT to_char(s1.username || '@' || s1.machine || ' ( SID=' || s1.sid || ' )  is blocking ' || s2.username || '@' || s2.machine || ' ( SID=' || s2.sid || ' ) ') retvalue 
    FROM v$lock l1, v$session s1, v$lock l2, v$session s2
    WHERE s1.sid=l1.sid AND s2.sid=l2.sid
    AND l1.BLOCK=1 AND l2.request > 0
    AND l1.id1 = l2.id1
    AND l2.id2 = l2.id2 
""")

	elif opc.lower() == 'enqueue':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'enqueue'
""")

	elif opc.lower() == 'dbseqread':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'db file sequential read
""")

	elif opc.lower() == 'dbscattread':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'db file scattered read'
""")

	elif opc.lower() == 'dbsnglwrite':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'db file single write'
""")

	elif opc.lower() == 'dbprllwrite':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'db file parallel write'
""")

	elif opc.lower() == 'directread':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'direct path read'
""")

	elif opc.lower() == 'directwrite':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'direct path write'
""")

	elif opc.lower() == 'latchfree':
		value = execute_command(cursor, """select to_char(time_waited, 'FM99999999999999990') retvalue
             from v$system_event se, v$event_name en
             where se.event(+) = en.name and en.name = 'latch free'
""")

	elif opc.lower() == 'tablespace':
		value = execute_command(cursor, """select 'Name:'|| tablespace_name,
        ' Used:',
         round(used_percent),
        '% |'
             from dba_tablespace_usage_metrics order by 3 desc
""")

	elif opc.lower() == 'alertatbs':
		value = execute_command(cursor, """select to_char(count(*), 'FM99999999999999990') retvalue from dba_tablespace_usage_metrics where USED_PERCENT > 80""")

	elif opc.lower() == 'list_tablespaces':
		value = execute_command(cursor, """select tablespace_name from dba_tablespaces""")

	return value