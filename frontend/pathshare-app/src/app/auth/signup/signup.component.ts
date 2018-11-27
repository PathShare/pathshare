import { Component, OnInit} from '@angular/core';
import { NgForm } from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor(private _authService: AuthService, private _router: Router) { }

  ngOnInit() {
  }

  onSignup(form: NgForm) {

    // userData: Json form of user's data
    const userData = JSON.stringify(form.value);

    this._authService.signupUser(userData)
      .subscribe(
        response => {
          console.log('success', response);
          const token = response['success'].slice(29, -1);
          localStorage.setItem('token', token);
          this._router.navigate(['/']);
        },
        error => console.log('error', error)
      );
  }

}
