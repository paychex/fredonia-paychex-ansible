
// Importing LUIS libraries
using Microsoft.Azure.CognitiveServices.Language.LUIS.Authoring;
using Microsoft.Azure.CognitiveServices.Language.LUIS.Authoring.Models;

using System;
using System.Collections.Generic;
using System.Linq;
using System.Security;
using System.Threading.Tasks;
using System.Windows.Forms;

using System.Web;

namespace Fredchex_AI
{
    struct ApplicationInfo
    {
        public Guid ID;
        public string Version;
    }

    static class Program
    {
        // Creating LUIS configuration variables. TODO: Hide
        // LUIS key:
        private static readonly string authorizing_key = "bde233f61f5e4e3fa48ff5a11b0f304c";
        // Region:
        private static readonly string region = "westus";
        // Endpoint:
        private static readonly string endpoint = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0";

        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());

            // Generating the credentials and creating the client
            var credentials = new Microsoft.Azure.CognitiveServices.Language.LUIS.Authoring.ApiKeyServiceClientCredentials(authorizing_key);
            var client = new LUISAuthoringClient(credentials, new System.Net.Http.DelegatingHandler[] { })
            {
                Endpoint = endpoint
            };
        }

        async static Task<ApplicationInfo> CreateApplication(LUISAuthoringClient client)
        {
            string app_name = String.Format("Fredchex AI");
            string app_description = "Terraform and Ansible assistant for Fredchex project";
            string app_version = "0.1";
            string app_culture = "en-us";

            var app_info = new ApplicationCreateObject()
            {
                Name = app_name,
                InitialVersionId = app_version,
                Description = app_description,
                Culture = app_culture
            };

            var app_id = await client.Apps.AddAsync(app_info);

            Console.WriteLine("Fredchex AI app {0} has been created\n with ID {1}", app_info.Name, app_id);

            return new ApplicationInfo() { ID= app_id, Version = app_version };
        }

        async static Task AddIntents(LUISAuthoringClient client, ApplicationInfo app_info)
        {
            await client.Model.AddIntentAsync(app_info.ID, app_info.Version, new ModelCreateObject()
            {
                Name = "CreateResource"
            });
            Console.WriteLine("Created intent CreateResource");
        }

        async static Task AddEntities(LUISAuthoringClient client, ApplicationInfo app_info)
        {
            var resourceCategoryEntityId = await client.Model.AddEntityAsync(app_info.ID, app_info.Version, new ModelCreateObject()
            {
                Name = "Resource Category"
            });

            await client.Model.CreateEntityRoleAsync(app_info.ID, app_info.Version, resourceCategoryEntityId, new EntityRoleCreateObject()
            {
                Name = "Resource Type"
            });

            await client.Model.CreateEntityRoleAsync(app_info.ID, app_info.Version, resourceCategoryEntityId,new EntityRoleCreateObject()
            {
                Name = "Number of Resource"
            });

            await client.Model.AddPrebuiltAsync(app_info.ID, app_info.Version, new List<string>
            {
                "keyPhrase",
                "number"
            });

            // Compositing the entities
            await client.Model.AddCompositeEntityAsync(app_info.ID, app_info.Version, new CompositeEntityModel()
            {
                Name = "Resource",
                Children = new List<string>()
                {
                    "Resource Category",
                    "Resource Type",
                    "number",
                    "keyPhrase"
                }
            });

            Console.WriteLine("Created entities Resource Category, Resoruce Type, number, keyPhrase.");
        }

        async static Task Train_App(LUISAuthoringClient client, ApplicationInfo app_info)
        {
            var response = await client.Train.TrainVersionAsync(app_info.ID, app_info.Version);
            Console.WriteLine("Training status: " + response.Status);
        }



    }
}
