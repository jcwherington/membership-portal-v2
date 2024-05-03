import { IconButton } from "@mui/material"
import CheckIcon from "@mui/icons-material/Check"
import ClearIcon from "@mui/icons-material/Clear"
import LogoutIcon from '@mui/icons-material/Logout';

const Types = {
    approve: {
        color: 'success',
        icon: <CheckIcon />
    },
    reject: {
        color: 'error',
        icon: <ClearIcon />
    },
    logout: {
        icon: <LogoutIcon />
    }
}

const SmallButtonComponent = (props: { handler: Function, data: any, type: string }): JSX.Element => {

    return (
        <IconButton
            color={Types[props.type].color}
            onClick={() =>
                props.handler(props.data)
            }
        >
            {Types[props.type].icon}
        </IconButton>
    )
}

export default SmallButtonComponent;
