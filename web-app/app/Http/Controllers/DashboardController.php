<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;

class DashboardController extends Controller
{
    public function view()
    {
        return Inertia::render('Dashboard/View', [
            'devices' => Auth::user()->devices,
        ]);
    }
}
