import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

// const httpOptions = {
//     headers: new HttpHeaders({
//       'content-type':  'application/json',

//     })
// }

@Injectable({
    providedIn: 'root'
})


export class AuthService {

    

    _url = 'http://35.203.92.65/post/user/new'

    constructor(private _http: HttpClient) {}

    // POST: Add new user to server 
    signupUser(userData) {

        const headers = new HttpHeaders()
          .set('Content-Type', 'application/json');

            console.log(userData)
            return this._http.post(this._url, userData, {headers : headers})
    }

    signinUser(email: string, password: string) {
        //sign up the user using backend
        console.log(email,password)
    }
}