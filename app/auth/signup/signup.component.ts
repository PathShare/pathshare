import { Component, OnInit} from '@angular/core';
import { NgForm } from '@angular/forms';
import { AuthService } from '../auth.service';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor(private _authService: AuthService) { }

  ngOnInit() {
  }

  onSignup(form: NgForm) {

    // userData: Json form of user's data
    const userData = JSON.stringify(form.value)

    this._authService.signupUser(userData)
      .subscribe(
        response => console.log("success",response),
        error => console.log("error", error)
      );
  }

}
