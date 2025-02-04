import { Button } from "@mui/material"
import AddIcon from "@mui/icons-material/Add"
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import DeleteIcon from '@mui/icons-material/Delete';

const Types = {
    approve: {
        color: 'success',
        icon: <AddIcon />
    },
    reject: {
        color: 'error',
        icon: <DeleteIcon />
    },
    cancel: {
        color: 'secondary',
        icon: <ArrowBackIcon />
    }
}

const LargeButtonComponent = (props: { children: string, type: string, handler: Function }): JSX.Element => {

    return (
        <Button
            variant="outlined"
            color={Types[props.type].color}
            endIcon={Types[props.type].icon}
            onClick={() => props.handler()}
            disableElevation
        > 
            {props.children}
        </Button>
    )
}

export default LargeButtonComponent;
