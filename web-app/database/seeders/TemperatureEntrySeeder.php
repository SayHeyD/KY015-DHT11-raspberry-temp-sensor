<?php

namespace Database\Seeders;

use App\Models\TemperatureEntry;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class TemperatureEntrySeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $dataPoints = 300;
        $previousEntry = null;

        for ($i = 0; $i < $dataPoints; $i++) {

            $measured_at = now()->subMinutes($dataPoints - $i);

            $tempEntry = TemperatureEntry::factory();

            if ($previousEntry != null) {
                $tempEntry = $tempEntry->tempRange(
                    $previousEntry->temperature - 2,
                    $previousEntry->temperature + 2
                );

                $tempEntry = $tempEntry->humidityRange(
                    $previousEntry->humidity - 0.5,
                    $previousEntry->humidity + 0.5
                );
            }

            $previousEntry = clone $tempEntry->create([
                'measured_at' => $measured_at->toString()
            ]);
        }
    }
}
