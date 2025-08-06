using Microsoft.EntityFrameworkCore;

namespace DataManager.Model
{
    public class DatabaseContext : DbContext
    {
        public DbSet<ElectricInfoDB> ElectricInfos { get; set; }
        public DatabaseContext(DbContextOptions<DatabaseContext> options) : base(options) { }
    }
}
