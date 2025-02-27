import jwt, { JwtPayload } from 'jsonwebtoken';
import { username, password, apiKey } from '../../config'

type Payload = {
    username: string,
    password: string
}

export function generateToken(payload: Payload): string {
    return jwt.sign(payload, apiKey(), { expiresIn: '1h' });
}
  
export function verifyToken(token: string): JwtPayload|string {
    try {
        return jwt.verify(token, apiKey());
    } catch (error) {
        return null;
    }
}

export function verifyCredentials(submittedUsername: string, submittedPassword: string): boolean {
    return submittedUsername === username() && submittedPassword === password();
}
