drop function if exists millis_to_duration;
delimiter $$
create function millis_to_duration(mil int)
returns varchar(300)
deterministic
begin
    declare f varchar(300);
    if (mil > 3599999) then
		set f = "%H:%i:%s";
	else
		set f = "%i:%s";
	end if;
    return time_format(sec_to_time(mil/1000), f);
end $$
delimiter ;

drop function if exists time_since_release;
delimiter $$
create function time_since_release(r_date date)
returns varchar(300)
deterministic
begin
    declare f varchar(300);
    declare days varchar(300);
    set days = datediff(curdate(), r_date);
    if (days > 7 and days <= 28) then
		set f = concat((days div 7), " weeks ago");
	elseif (days > 28 and days <= 360) then
		set f = concat((days div 30), " months ago");
	else
		set f = concat((days div 360), " years ago");
	end if;
    return f;
end $$
delimiter ;