import '@/styles/globals.css'
import NavBar from '@/components/NavBar'
import type { AppProps } from 'next/app'
import { useRouter, NextRouter } from 'next/router';
import cookieCutter from 'cookie-cutter'
import { useState, useEffect } from 'react';
import { Inter } from 'next/font/google'
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { ThemeProvider, createTheme, Theme } from '@mui/material/styles';
import User from '@/model/user';
import { NextFont } from 'next/dist/compiled/@next/font';


const inter: NextFont = Inter({ subsets: ['latin'] })

const theme: Theme = createTheme({
  palette: {
    secondary: {
      main: '#57C4CA',
    },
  },
});

export default function App({ Component, pageProps }: AppProps): JSX.Element {
  const router: NextRouter = useRouter();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = cookieCutter.get('token');

    if (!user) {
      setUser(new User(token));
    }
  }, [user]);

  if (user && !user.isValid()) {
    cookieCutter.set('token', '', { expires: new Date(0) });
    router.push('/index.html');
  }

  return (
    <ThemeProvider theme={theme}>
      <LocalizationProvider dateAdapter={AdapterDayjs} >
        <main className={inter.className} >
            {user?.isValid() ?
              <NavBar>
                <Component {...pageProps} />
              </NavBar>
            :
              <Component {...pageProps} />}
        </main>
      </LocalizationProvider>
    </ThemeProvider>
  )
}
