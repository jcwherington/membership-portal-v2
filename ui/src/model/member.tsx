import { DATE_FORMAT, TIMESTAMP_FORMAT } from '@/lib/constants';
import dayjs from 'dayjs';

class Member {
    private readonly id: number
    private readonly firstName: string;
    private readonly lastName: string;
    private readonly organisation: string;
    private readonly position: string;
    private readonly industry: string;
    private readonly email: string;
    private readonly dob: string;
    private readonly city: string;
    private readonly mobile: string;
    private readonly postCode: string;
    private readonly createdAt: string;
    private readonly updatedAt: string;

    constructor(props: any) {
        this.id = props.id
        this.firstName = props.firstName;
        this.lastName = props.lastName;
        this.organisation = props.organisation;
        this.position = props.position;
        this.industry = props.industry;
        this.email = props.email;
        this.dob = dayjs.isDayjs(props.dob) ? props.dob.format(DATE_FORMAT) : props.dob;
        this.city = props.city;
        this.mobile = props.mobile;
        this.postCode = props.postCode;
        this.createdAt = dayjs(props.createdAt).format(TIMESTAMP_FORMAT);
        this.updatedAt = dayjs(props.updatedAt).format(TIMESTAMP_FORMAT);
    }

    getId() {
        return this.id;
    }

    getFirstName() {
        return this.firstName;
    }
    
    getLastName() {
        return this.lastName;
    }
    
    getOrganisation() {
        return this.organisation;
    }
    
    getPosition() {
        return this.position;
    }
    
    getIndustry() {
        return this.industry;
    }
    
    getEmail() {
        return this.email;
    }
  
    getDOB() {
        return dayjs(this.dob, DATE_FORMAT);
    }

    getCity() {
        return this.city;
    }
    
    getMobile() {
        return this.mobile;
    }
    
    getPostCode() {
        return this.postCode;
    }

    getDateCreated() {
        return this.createdAt;
    }
    
    getDateUpdated() {
        return this.updatedAt;
    }

    getName() {
        return `${this.firstName} ${this.lastName}`;
    }

    identify(value: string) {
        const fullName = this.getName().toLowerCase();
        const lastName = this.getLastName().toLowerCase();
        const filterText = value.toLowerCase();

        return fullName.startsWith(filterText) || lastName.startsWith(filterText);
    }

    compare(member: Member) {
        const date = dayjs(this.getDateCreated());
        const comparedDate = dayjs(member.getDateCreated());

        if(date.isSame(comparedDate)) return 0;
        return date.isBefore(comparedDate) ? 1 : -1;
    }
}

export default Member
