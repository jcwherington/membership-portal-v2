import {NextRouter, useRouter} from 'next/router';
import cookieCutter from 'cookie-cutter'
import { useState, useEffect } from 'react';
import { verifyCredentials, generateToken } from '@/lib/auth';
import Login from '@/components/Login';
import ErrorComponent from '@/components/Error';

export default function Home(): JSX.Element {
  const router: NextRouter = useRouter();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const token: string = cookieCutter.get('token');

    if (token) {
      router.push('/admin.html');
    }
  }, [router]);

  const handleLogin: Function = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const login = event.target as HTMLFormElement
    const username: string = login.username.value;
    const password: string = login.password.value;

    if (verifyCredentials(username, password)) {
      const token = generateToken({
        username: username, 
        password: password
      });
      
      cookieCutter.set('token', token);

      router.push('/admin.html');
    } 
    else {
      setErrorMessage('Login failed! Please check your credentials');
    }
  };

  return (
    <>
      {errorMessage && <ErrorComponent message={errorMessage}/>}
      <Login handler={handleLogin} />
    </>
  )
}
