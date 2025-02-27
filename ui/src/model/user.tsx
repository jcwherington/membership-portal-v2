import { JwtPayload } from 'jsonwebtoken';
import { verifyToken } from '@/lib/auth';

class User {
    private _isLoggedIn: boolean
    private _expiry: number

    constructor(token: string) {
        const decodedToken = verifyToken(token) as JwtPayload;

        this._isLoggedIn = Boolean(decodedToken);
        this._expiry = decodedToken?.exp;
    }

    isLoggedIn(): boolean {
        return this._isLoggedIn;
    }

    isExpired(): boolean {
        return  Date.now() >= (this._expiry * 1000);
    }

    isValid(): boolean {
        return this.isLoggedIn() && !this.isExpired()
    }
}

export default User;
