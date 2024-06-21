-- Definición del huevo
local modpath = minetest.get_modpath(minetest.get_current_modname())
local egg_name = "xpd_albanil:building_egg"
local egg_texture = modpath .. "/textures/egg_texture.png" -- Reemplaza con la ruta de tu textura
local egg_description = "Un huevo mágico que construye bloques a partir de una URL"

local request_api = minetest.request_http_api()
local json = loadfile(modpath .. "/json.lua")()

-- Manejo del clic derecho
local function xpdegg_after_place_node(pos, placer, itemstack, pointed_thing)
    local meta = minetest.get_meta(pos)
    meta:set_string("formspec",
            "size[5,3]"..
            "field[0,1;5,1;url;Ingrese URL;]"
            )
end

local function xpdegg_on_receive_fields(pos, formname, fields, player)
    if fields.url == nil then
        return
    end
    local mi_url = string.trim(fields.url)
    if mi_url == "" then
        return
    end
    
    if request_api == nil then
        minetest.chat_send_player( player:get_player_name() , "Http Requests are disabled or unauthorized")
        return
    end

    minetest.chat_send_player( player:get_player_name() , "Typed: " .. mi_url)

    request_api.fetch({ url = mi_url, timeout = 10 }, function(respuesta)
        -- minetest.chat_send_player( player:get_player_name() , "Respuesta: " .. json.encode(respuesta) )
        if not respuesta.succeeded then
            minetest.chat_send_player( player:get_player_name() , "Peticion no exitosa" )
            return
        elseif respuesta.code ~= 200 then
            minetest.chat_send_player( player:get_player_name() , "Respuesta HTTP " .. to_string(respuesta.code) )
            return
        end
        local data = json.decode(respuesta.data)
        if data == nil or data.bloques == nil then
            minetest.chat_send_player( player:get_player_name() , "Respuesta de sitio no cumple con el formato" )
            return
        end
        minetest.chat_send_player( player:get_player_name() , "Inicia construccion de modelo: " .. data.nombre )
        for indice, bloque in pairs(data.bloques) do
            minetest.chat_send_player( player:get_player_name() , "Procesando bloque " .. json.encode(bloque) )
            local pos_bloque = { x = pos.x + bloque.x, y = pos.y + bloque.y, z = pos.z + bloque.z}
            local info_bloque = { name = bloque.tipo_bloque }
            minetest.set_node(pos_bloque, info_bloque)
        end
    end)
end

--minetest.register_item(
minetest.register_node(
    egg_name,
    {
        description = egg_description,
        w = 1,
        h = 1,
        image = egg_texture,
        stack = 64,
        after_place_node = xpdegg_after_place_node,
        on_receive_fields = xpdegg_on_receive_fields
    }
)