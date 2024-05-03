import { Button } from "@mui/material"
import Papa from 'papaparse';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import Member from '@/model/member'
import { isBetween } from '@/lib/date';


const ExportButtonComponent = (props: { data: Member[], startDate: string, endDate: string }): JSX.Element => {
    const exportToCSV = function () {
        const filteredData = props.data.filter((member) => isBetween(member.getDateCreated(), props.startDate, props.endDate));
        const csv = Papa.unparse(filteredData, {
            header: true,
            quotes: true
        })
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `member_export_${Date.now()}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    return (
        <Button
            variant="outlined"
            color="secondary" 
            onClick={() => exportToCSV()}
            endIcon={<FileDownloadIcon />}
        > 
            Export
        </Button>
    )
}

export default ExportButtonComponent;
