import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ShareMyTripComponent } from './share-my-trip.component';

describe('ShareMyTripComponent', () => {
  let component: ShareMyTripComponent;
  let fixture: ComponentFixture<ShareMyTripComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ShareMyTripComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ShareMyTripComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
