import { ChangeEvent, useState } from 'react';
import LargeButton from '@/components/buttons/LargeButton';
import ExportButton from '@/components/buttons/ExportButton';
import { DateField } from '@mui/x-date-pickers';
import { useRouter, NextRouter } from 'next/router';
import Member from '@/model/member';
import { DATE_FORMAT } from '@/lib/constants';

const TableSubHeaderComponent = (props: {onFilter: Function, data: Member[]}): JSX.Element => {
    const router: NextRouter = useRouter();
    const [startDate, setStartDate] = useState<string | null>(null)
    const [endDate, setEndDate] = useState<string | null>(null)

    const createHandler: Function = () => {
        router.push({pathname: '/admin/member/create.html'});
    }

    return (
        <>
            <div style={{ display: 'flex', justifyContent: 'flex-start', width: '50%'}}>
                <div style={{ paddingRight: '1em' }}>
                    <input 
                        type='text'
                        id='filter'
                        name='filter'
                        placeholder='Search'
                        onChange={(e: ChangeEvent<HTMLInputElement>) => props.onFilter(e.target.value)}
                    />
                </div>
                <div>
                    <LargeButton type='approve' handler={createHandler}>
                        Create
                    </LargeButton>
                </div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'flex-end', width: '50%'}}>
                <p style={{ margin: '0.5em' }}>Start Date: </p>
                <div style={{ paddingRight: '1em' }} >
                    <DateField
                        name='startDate'
                        label={DATE_FORMAT}
                        value={''}
                        onChange={(newValue) => setStartDate(newValue)}
                        format={DATE_FORMAT}
                    />
                </div>
                <p style={{ margin: '0.5em' }}>End Date: </p>
                <div style={{ paddingRight: '1em' }}>
                    <DateField 
                        name='endDate'
                        label={DATE_FORMAT}
                        value={''}
                        onChange={(newValue) => setEndDate(newValue)}
                        format={DATE_FORMAT}
                    />
                </div>
                <div>
                    <ExportButton 
                        data={props.data}
                        startDate={startDate}
                        endDate={endDate}
                    />
                </div>
            </div>
        </>
    );
};

export default TableSubHeaderComponent;
