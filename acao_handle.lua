-- Code snippet is inteded to handle ACAO deny/allow based on origin header value or referer header.

local domains = [[yahoo.com|google.com|apple.com]]

function acao_handle()
    
    -- get headers
    local oheader = get_request_header_value("Origin")
    local rheader = get_request_header_value("Referer")

    -- validate origin header
    if oheader then
        if oheader == "" then
            log_debug("Authorized: Blank Origin Header")
            return
        elseif request_header_match("Origin", domains, false) then
            log_debug("Authorized via Origin: " .. oheader)
            return
        else
            log_debug("Not Authorized via Origin: " .. oheader)
        end
    end

    -- validate referer header
    if rheader then
        if rheader == "" then
            log_debug("Authorized: Blank Referer Header")
            return
        elseif request_header_match("Referer", domains, false) then
            log_debug("Authorized via Referer: " .. rheader)
            return
        else
            log_debug("Not Authorized via Referer: " .. rheader)
        end
    end

    -- check if no headers are present
    if not oheader and not rheader then
        log_debug("Authorized: No header")
        return  
    end

    -- validation failure
    log_debug("403 Not Authorized")
    generate_response(403)
end
