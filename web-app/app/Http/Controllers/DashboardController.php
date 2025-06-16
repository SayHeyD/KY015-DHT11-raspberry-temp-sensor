<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;

class DashboardController extends Controller
{
    public function view(Request $request)
    {
        $devices = Auth::user()->devices;

        $selectedDevice = $request->query('device');

        return Inertia::render('Dashboard/View', [
            'devices' => fn () => $devices->load([
                'temperatures' => function($query) {
                    $query
                        ->where('created_by', '>=', now()->subDay())
                        ->orderBy('created_at', 'desc');
                }
            ]),
            'selectedDeviceId' => $selectedDevice
        ]);
    }
}
