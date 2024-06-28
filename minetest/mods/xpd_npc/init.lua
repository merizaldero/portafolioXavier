local path = minetest.get_modpath(minetest.get_current_modname()) .. "/"

-- Check for translation method
local S
if minetest.get_translator ~= nil then
    print("xpd_npc: 5.x translation function")
	S = minetest.get_translator("xpd_npc") -- 5.x translation function
else
	if minetest.get_modpath("intllib") then
        print("xpd_npc: intllib translation function")
		dofile(minetest.get_modpath("intllib") .. "/init.lua")
		if intllib.make_gettext_pair then
			S = intllib.make_gettext_pair() -- new gettext method
		else
			S = intllib.Getter() -- old text file method
		end
	else -- boilerplate function
        print("xpd_npc: translation boilerplate function")
		S = function(str, ...)
			local args = {...}
			return str:gsub("@%d+", function(match)
				return args[tonumber(match:sub(2))]
			end)
		end
	end
end

xpd_npc = {S = S}

-- NPCs
dofile(path .. "simio.lua") -- TenPlus1
dofile(path .. "waifu.lua") -- TenPlus1
