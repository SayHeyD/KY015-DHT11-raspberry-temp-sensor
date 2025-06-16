<?php

namespace Database\Factories;

use App\Models\Device;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\TemperatureEntry>
 */
class TemperatureEntryFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'device_id' => Device::all()->random()->id,
            'temperature' => $this->faker->randomFloat(1, -20, 50),
            'humidity' => $this->faker->randomFloat(1, 0, 100),
            'measured_at' => now()->toString(),
            'mock' => true,
        ];
    }

    public function tempRange(float $minTemp, float $maxTemp): TemperatureEntryFactory
    {
        if ($minTemp < -20) $minTemp = -20;
        if ($maxTemp > 50) $maxTemp = 50;

        return $this->state(function (array $attributes) use ($minTemp, $maxTemp) {
            return [
                'temperature' => $this->faker->randomFloat(1, $minTemp, $maxTemp),
            ];
        });
    }

    public function humidityRange(float $minHumidity, float $maxHumidity): TemperatureEntryFactory
    {
        if ($minHumidity < 0) $minHumidity = 0;
        if ($minHumidity > 100) $maxHumidity = 100;

        return $this->state(function (array $attributes) use ($minHumidity, $maxHumidity) {
            return [
                'humidity' => $this->faker->randomFloat(1, $minHumidity, $maxHumidity),
            ];
        });
    }
}
