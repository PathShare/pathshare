import { User } from './../shared/model/user';
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

    

    _rootUrl = 'http://104.199.173.34'

    constructor(private _http: HttpClient) {}

    // POST: Add new user to server 
    // Test Email: bitegizi@xcodes.net
    // Test Pass: aaaaaaaaa
    signupUser(userData) {

        const headers = new HttpHeaders()
          .set('Content-Type', 'application/json');

            console.log(userData)
            return this._http.post(this._rootUrl + '/post/user/new', userData, {headers : headers})
    }

    signinUser(userEmail): Observable<User>{

        const headers = new HttpHeaders()
        .set('Content-Type', 'application/json');

        return this._http.get<User>(this._rootUrl + '/get/user?email=' + userEmail, {headers : headers})
    }
}