import styles from '@/styles/Error.module.css';
import ErrorOutlineOutlinedIcon from '@mui/icons-material/ErrorOutlineOutlined';

const Error = (props: { message: string }): JSX.Element => {

    return (
        <div className={styles.container}>
            <div className={styles.icon}>
                <ErrorOutlineOutlinedIcon style={{ color: 'white' }} />
            </div>
            <p className={styles.errorText}>{props.message}</p>
        </div>
    )
}

export default Error;
