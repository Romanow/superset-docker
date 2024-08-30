const baseURL = process.env.REACT_APP_SUPERSET_URL;

type AccessToken = {
    access_token: string
}

type GuestToken = {
    token: string
}

export const Api = {
    token: async (username: String, password: String, dashboardId: String): Promise<string> => {
        const body = {"username": username, "password": password, "provider": "ldap"};
        return await fetch(`${baseURL}/api/v1/security/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8"
            },
            body: JSON.stringify(body)
        })
            .then(response => response.json() as Promise<AccessToken>)
            .then(json => Api.guestToken(json.access_token, dashboardId))
    },
    guestToken: async (token: String, dashboardId: String): Promise<string> => {
        const body = {
            "user": {"username": "guest_user"},
            "resources": [{"type": "dashboard", "id": dashboardId}],
            "rls": []
        };
        return await fetch(`${baseURL}/api/v1/security/guest_token/`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json;charset=utf-8"
            },
            body: JSON.stringify(body),
        })
            .then(response => response.json() as Promise<GuestToken>)
            .then(json => json.token)
    }
}
