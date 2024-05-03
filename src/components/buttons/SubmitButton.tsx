import { Button } from "@mui/material"
import AddIcon from "@mui/icons-material/Add"

const SubmitButtonComponent = (props: { children: string }): JSX.Element => {

    return (
        <Button
            type="submit"
            variant="outlined"
            color="success"
            endIcon={<AddIcon />}
            disableElevation
        > 
            {props.children}
        </Button>
    )
}

export default SubmitButtonComponent;
