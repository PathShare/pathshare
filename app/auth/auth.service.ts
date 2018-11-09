export class AuthService {
    signupUser(name: string, major: string, age: number, username:string,
        email: string, password: string) {

            //sign up the user using backend
            console.log(name,major,age,username,email,password)

    }

    signinUser(email: string, password: string) {
        //sign up the user using backend
        console.log(email,password)
    }
}