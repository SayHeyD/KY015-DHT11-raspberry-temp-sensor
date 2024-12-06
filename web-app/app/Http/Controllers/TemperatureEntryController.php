<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreTemperatureEntryRequest;
use App\Models\Device;
use App\Models\TemperatureEntry;
use Illuminate\Support\Facades\Auth;

class TemperatureEntryController extends Controller
{
    public function store(StoreTemperatureEntryRequest $request)
    {
        $device = Auth::user();

        if (! $device instanceof Device) {
            return response()
                ->json(
                    [
                        'message' => 'Temperature entries must be created by devices.'
                    ],
                    403
                );
        }

        $tempEntry = TemperatureEntry::create([
            'device_id' => $device->id,
            'temperature' => $request->temperature,
            'humidity' => $request->humidity,
        ]);

        return response()->json(['id' => $tempEntry->id],201);
    }
}
