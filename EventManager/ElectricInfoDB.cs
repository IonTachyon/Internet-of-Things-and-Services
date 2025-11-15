using System.ComponentModel.DataAnnotations;
namespace DataManager.Model
{
    public class ElectricInfoDB
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public required DateOnly Date { get; set; }

        [Required]
        public required TimeOnly Time { get; set; }

        [Required]
        public required float Global_active_power { get; set; }

        [Required]
        public required float Global_reactive_power { get; set; }

        [Required]
        public required float Voltage { get; set; }

        [Required]
        public required float Global_intensity { get; set; }

        [Required]
        public required float Sub_metering_1 { get; set; }

        [Required]
        public required float Sub_metering_2 { get; set; }

        [Required]
        public required float Sub_metering_3 { get; set; }
    }
}
